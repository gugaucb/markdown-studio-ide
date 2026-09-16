import os
import zipfile
import tempfile
import shutil
import json
import csv
import re
from typing import Optional, Dict, Any, List
import requests
from bs4 import BeautifulSoup

try:
    from markitdown import MarkItDown
except ImportError:
    MarkItDown = None

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

try:
    from youtube_transcript_api import YouTubeTranscriptApi
except ImportError:
    YouTubeTranscriptApi = None

try:
    import extract_msg
except ImportError:
    extract_msg = None

try:
    import feedparser
except ImportError:
    feedparser = None

try:
    import wikipediaapi
except ImportError:
    wikipediaapi = None

try:
    import pymupdf4llm
except ImportError:
    pymupdf4llm = None


class LLMTrackingWrapper:
    """Intercepta e contabiliza chamadas ao cliente OpenAI durante a conversão."""
    def __init__(self, client):
        self._client = client
        self.call_count = 0
        self.last_model_used = None

    def reset(self):
        self.call_count = 0
        self.last_model_used = None

    @property
    def was_called(self) -> bool:
        return self.call_count > 0

    def __getattr__(self, name):
        if name == "chat":
            return ChatWrapper(self, getattr(self._client, "chat"))
        return getattr(self._client, name)


class ChatWrapper:
    def __init__(self, tracker: LLMTrackingWrapper, chat_obj):
        self._tracker = tracker
        self._chat = chat_obj

    @property
    def completions(self):
        return CompletionsWrapper(self._tracker, getattr(self._chat, "completions"))

    def __getattr__(self, name):
        return getattr(self._chat, name)


class CompletionsWrapper:
    def __init__(self, tracker: LLMTrackingWrapper, completions_obj):
        self._tracker = tracker
        self._completions = completions_obj

    def create(self, *args, **kwargs):
        self._tracker.call_count += 1
        self._tracker.last_model_used = kwargs.get("model")
        return self._completions.create(*args, **kwargs)

    def __getattr__(self, name):
        return getattr(self._completions, name)


class MarkItDownService:
    def __init__(self, openai_api_key: Optional[str] = None, llm_model: str = "gemma4:26b", openai_base_url: Optional[str] = "http://127.0.0.1:11434/v1"):
        self.openai_api_key = openai_api_key
        self.llm_model = llm_model or "gemma4:26b"
        self.openai_base_url = openai_base_url
        self.llm_client = None
        self.tracker = None
        self._init_converter()

    def _clean_base_url(self, url: Optional[str]) -> Optional[str]:
        if not url:
            return None
        url = url.strip().rstrip("/")
        if not url:
            return None
        # Normaliza localhost:11434 para 127.0.0.1:11434 no Windows para evitar falhas de resolução IPv6
        if "://localhost:11434" in url:
            url = url.replace("://localhost:11434", "://127.0.0.1:11434")
        return url

    def _init_converter(self):
        if MarkItDown is None:
            self.md = None
            self.llm_client = None
            self.tracker = None
            return

        cleaned_base_url = self._clean_base_url(self.openai_base_url)

        # Determina a chave efetiva
        api_key = self.openai_api_key
        if api_key:
            api_key = api_key.strip()

        # Se tiver base_url configurada e a api_key estiver vazia (típico de Ollama / LM Studio local),
        # usamos um placeholder para que o SDK OpenAI não lance exceção de validação
        if cleaned_base_url and not api_key:
            api_key = "ollama"

        if (api_key or cleaned_base_url) and OpenAI is not None:
            client_kwargs = {"api_key": api_key or "ollama", "timeout": 180.0}
            if cleaned_base_url:
                client_kwargs["base_url"] = cleaned_base_url

            raw_client = OpenAI(**client_kwargs)
            self.tracker = LLMTrackingWrapper(raw_client)
            self.llm_client = self.tracker
            self.md = MarkItDown(llm_client=self.llm_client, llm_model=self.llm_model)
            # Injeta diretamente no MarkItDown para garantir visibilidade nos conversores
            self.md._llm_client = self.llm_client
            self.md._llm_model = self.llm_model
        else:
            self.llm_client = None
            self.tracker = None
            self.md = MarkItDown()

    def update_config(self, openai_api_key: Optional[str] = None, llm_model: Optional[str] = None, openai_base_url: Optional[str] = None):
        if openai_api_key is not None:
            self.openai_api_key = openai_api_key.strip() if openai_api_key else None
        if llm_model is not None:
            self.llm_model = llm_model.strip() if llm_model else "gemma4:26b"
        if openai_base_url is not None:
            self.openai_base_url = self._clean_base_url(openai_base_url)
        self._init_converter()

    def refine_markdown_with_llm(self, markdown: str, filename: str, ext: str) -> str:
        """Uses LLM to polish and enrich markdown structure, tables, and hierarchy for documents."""
        if not self.llm_client or not markdown or not markdown.strip():
            return markdown

        sample_text = markdown[:14000]
        prompt = (
            f"You are an expert technical editor and Markdown structure specialist.\n"
            f"The following content was extracted from '{filename}' ({ext}).\n"
            f"Your mission is to polish, structure, and refine this Markdown document adhering to these mandatory guidelines:\n\n"
            f"1. ENCODING & CHARACTER CORRUPTION REPAIR (CRITICAL):\n"
            f"   - Detect and rectify any character encoding anomalies, mojibake artifacts (e.g., 'Ã§Ã£o' -> 'ação', 'Ã©' -> 'é', 'Ã¡' -> 'á', 'Ãº' -> 'ú', etc.), misdecoded byte sequences, and broken Unicode symbols.\n"
            f"   - Restore correct grammatical accents, diacritics, and punctuation matching the document's native language.\n"
            f"   - Fix words accidentally split or truncated by OCR, PDF line wrapping, or hyphenation (e.g., 'desen- volvimento' -> 'desenvolvimento').\n\n"
            f"2. STRUCTURAL HIERARCHY & FORMATTING:\n"
            f"   - Organize headings hierarchically (#, ##, ###) logically based on the document flow.\n"
            f"   - Format lists, bullet points, and code blocks cleanly.\n"
            f"   - Eliminate artificial mid-sentence line breaks while maintaining clean paragraph spacing.\n\n"
            f"3. STRICT TABLE PRESERVATION:\n"
            f"   - If the document contains Markdown tables (| col1 | col2 |), you MUST PRESERVE all tables, columns, headers, rows, and cells verbatim. NEVER convert tables to plain text, bullet lists, or summary blocks.\n\n"
            f"4. ABSOLUTE DATA INTEGRITY:\n"
            f"   - Maintain all facts, figures, dates, proper nouns, URLs, and code snippets with zero alteration or hallucinations.\n\n"
            f"5. OUTPUT FORMAT:\n"
            f"   - Return ONLY the clean, refined Markdown text. Do NOT include greetings, preamble, explanations, or wrapping markdown codeblocks (such as ```markdown ... ```)."
        )

        try:
            response = self.llm_client.chat.completions.create(
                model=self.llm_model,
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": sample_text}
                ],
                max_tokens=4000
            )
            msg = response.choices[0].message
            refined = (msg.content or "").strip()
            
            # Se o modelo gerou apenas reasoning ou conteúdo vazio, preserva o original
            if not refined and hasattr(msg, "reasoning") and msg.reasoning:
                return markdown

            if refined:
                if refined.startswith("```markdown") and refined.endswith("```"):
                    refined = refined[len("```markdown"): -3].strip()
                elif refined.startswith("```") and refined.endswith("```"):
                    refined = refined[3:-3].strip()
                
                # Salvaguarda: se o texto original possuía tabelas formatadas e o modelo as removeu, preserva original
                if "|---|" in sample_text and "|---|" not in refined:
                    return markdown

                if len(markdown) > 14000:
                    refined += "\n\n*(Conteúdo restante mantido na íntegra)*\n\n" + markdown[14000:]
                return refined
        except Exception:
            pass

        return markdown

    def convert_file(self, file_path: str, filename: Optional[str] = None, use_llm: bool = True) -> Dict[str, Any]:
        """Converts a local file to Markdown based on its extension."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Arquivo nao encontrado: {file_path}")

        name = filename or os.path.basename(file_path)
        ext = os.path.splitext(name)[1].lower()

        # Reseta tracker de telemetria antes de converter
        if self.tracker:
            self.tracker.reset()

        # Garante repasse explícito do cliente e modelo LLM apenas se use_llm for True
        convert_kwargs = {}
        if use_llm and self.llm_client is not None:
            convert_kwargs["llm_client"] = self.llm_client
            convert_kwargs["llm_model"] = self.llm_model
            if self.md:
                self.md._llm_client = self.llm_client
                self.md._llm_model = self.llm_model
        else:
            if self.md:
                self.md._llm_client = None
                self.md._llm_model = None

        # Handle ZIP Archives recursively
        if ext == ".zip":
            res = self._convert_zip_archive(file_path, name, use_llm=use_llm)
            llm_used = self.tracker.was_called if (use_llm and self.tracker) else False
            res["llm_used"] = llm_used
            res["llm_model"] = self.llm_model if llm_used else None
            res["llm_provider"] = (self.openai_base_url or "https://api.openai.com/v1") if llm_used else None
            res["llm_calls_count"] = self.tracker.call_count if (llm_used and self.tracker) else 0
            return res

        # Handle Outlook .msg files
        if ext == ".msg":
            res = self._convert_msg_file(file_path, name)
            if use_llm and self.llm_client is not None and res.get("markdown"):
                res["markdown"] = self.refine_markdown_with_llm(res["markdown"], name, ext)
            llm_used = self.tracker.was_called if (use_llm and self.tracker) else False
            res["llm_used"] = llm_used
            res["llm_model"] = self.llm_model if llm_used else None
            res["llm_provider"] = (self.openai_base_url or "https://api.openai.com/v1") if llm_used else None
            res["llm_calls_count"] = self.tracker.call_count if (llm_used and self.tracker) else 0
            return res

        # Handle Data Formats fallback
        if ext in [".json", ".csv", ".xml"]:
            res = self._convert_data_format(file_path, name, ext)
            if use_llm and self.llm_client is not None and res.get("markdown"):
                res["markdown"] = self.refine_markdown_with_llm(res["markdown"], name, ext)
            llm_used = self.tracker.was_called if (use_llm and self.tracker) else False
            res["llm_used"] = llm_used
            res["llm_model"] = self.llm_model if llm_used else None
            res["llm_provider"] = (self.openai_base_url or "https://api.openai.com/v1") if llm_used else None
            res["llm_calls_count"] = self.tracker.call_count if (llm_used and self.tracker) else 0
            return res

        # Handle PDF documents with high-accuracy table & layout preservation
        if ext == ".pdf":
            return self._convert_pdf_file(file_path, name, use_llm=use_llm, convert_kwargs=convert_kwargs)

        # Standard conversion using MarkItDown
        if self.md:
            try:
                result = self.md.convert(file_path, **convert_kwargs)
                text_content = result.text_content if hasattr(result, "text_content") else str(result)

                # Se use_llm estiver ativo e o conversor do MarkItDown ainda nao tiver acionado o LLM
                # (ex: para documentos PDF, DOCX, XLSX, TXT), aplica o refinamento textual universal
                is_image_or_multimodal = ext in [".png", ".jpg", ".jpeg", ".webp", ".bmp", ".gif"]
                if use_llm and self.llm_client is not None and not is_image_or_multimodal and text_content.strip():
                    text_content = self.refine_markdown_with_llm(text_content, name, ext)

                llm_used = self.tracker.was_called if (use_llm and self.tracker) else False
                return {
                    "filename": name,
                    "extension": ext,
                    "markdown": text_content,
                    "type": "file",
                    "engine": "markitdown",
                    "llm_used": llm_used,
                    "llm_model": self.llm_model if llm_used else None,
                    "llm_provider": (self.openai_base_url or "https://api.openai.com/v1") if llm_used else None,
                    "llm_calls_count": self.tracker.call_count if (llm_used and self.tracker) else 0
                }
            except Exception as e:
                res = self._fallback_file_convert(file_path, name, ext, str(e))
                res["engine"] = "fallback"
                if use_llm and self.llm_client is not None and res.get("markdown"):
                    res["markdown"] = self.refine_markdown_with_llm(res["markdown"], name, ext)
                llm_used = self.tracker.was_called if (use_llm and self.tracker) else False
                res["llm_used"] = llm_used
                res["llm_model"] = self.llm_model if llm_used else None
                res["llm_provider"] = (self.openai_base_url or "https://api.openai.com/v1") if llm_used else None
                res["llm_calls_count"] = self.tracker.call_count if (llm_used and self.tracker) else 0
                return res
        else:
            res = self._fallback_file_convert(file_path, name, ext, "MarkItDown library not initialized")
            res["engine"] = "fallback"
            res["llm_used"] = False
            res["llm_model"] = None
            res["llm_provider"] = None
            res["llm_calls_count"] = 0
            return res

    def _convert_pdf_file(self, file_path: str, name: str, use_llm: bool = True, convert_kwargs: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Converts a PDF file using PyMuPDF4LLM for high-accuracy table & layout preservation, with fallback to MarkItDown."""
        text_content = None
        engine_used = "markitdown"

        if pymupdf4llm is not None:
            try:
                text_content = pymupdf4llm.to_markdown(file_path)
                engine_used = "pymupdf4llm"
            except Exception:
                text_content = None

        if text_content is None:
            if self.md:
                try:
                    kwargs = convert_kwargs or {}
                    result = self.md.convert(file_path, **kwargs)
                    text_content = result.text_content if hasattr(result, "text_content") else str(result)
                    engine_used = "markitdown"
                except Exception as e:
                    return self._fallback_file_convert(file_path, name, ".pdf", str(e))
            else:
                return self._fallback_file_convert(file_path, name, ".pdf", "No PDF conversion engine available")

        if use_llm and self.llm_client is not None and text_content and text_content.strip():
            text_content = self.refine_markdown_with_llm(text_content, name, ".pdf")

        llm_used = self.tracker.was_called if (use_llm and self.tracker) else False
        return {
            "filename": name,
            "extension": ".pdf",
            "markdown": text_content,
            "type": "file",
            "engine": engine_used,
            "llm_used": llm_used,
            "llm_model": self.llm_model if llm_used else None,
            "llm_provider": (self.openai_base_url or "https://api.openai.com/v1") if llm_used else None,
            "llm_calls_count": self.tracker.call_count if (llm_used and self.tracker) else 0
        }

    def _convert_zip_archive(self, zip_path: str, name: str, use_llm: bool = True) -> Dict[str, Any]:
        """Recursively extracts and converts contents of a ZIP archive."""
        temp_dir = tempfile.mkdtemp(prefix="markitdown_zip_")
        try:
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)

            converted_items = []
            markdown_parts = [f"# Arquivo ZIP: {name}\n", "## Estrutura do Arquivo Concatenado\n"]

            for root, _, files in os.walk(temp_dir):
                for f in files:
                    full_path = os.path.join(root, f)
                    rel_path = os.path.relpath(full_path, temp_dir)
                    
                    if f.startswith(".") or f.startswith("__MACOSX"):
                        continue

                    try:
                        res = self.convert_file(full_path, filename=rel_path, use_llm=use_llm)
                        md_content = res.get("markdown", "")
                        converted_items.append({
                            "path": rel_path,
                            "markdown": md_content
                        })
                        markdown_parts.append(f"### File: `{rel_path}`\n\n{md_content}\n\n---\n")
                    except Exception as err:
                        markdown_parts.append(f"### File: `{rel_path}` *(Erro na conversao: {err})*\n\n---\n")

            full_markdown = "\n".join(markdown_parts)
            return {
                "filename": name,
                "extension": ".zip",
                "markdown": full_markdown,
                "type": "archive",
                "item_count": len(converted_items),
                "items": converted_items
            }
        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)

    def _convert_msg_file(self, file_path: str, name: str) -> Dict[str, Any]:
        """Extracts content from Microsoft Outlook .msg files."""
        if extract_msg is not None:
            try:
                msg = extract_msg.Message(file_path)
                subject = msg.subject or "Sem Assunto"
                sender = msg.sender or "Desconhecido"
                date = msg.date or "Data nao especificada"
                body = msg.body or ""

                md_out = f"# Email: {subject}\n\n"
                md_out += f"- **De:** {sender}\n"
                md_out += f"- **Data:** {date}\n"
                if msg.to:
                    md_out += f"- **Para:** {msg.to}\n"
                md_out += "\n---\n\n"
                md_out += body.strip()

                return {
                    "filename": name,
                    "extension": ".msg",
                    "markdown": md_out,
                    "type": "email"
                }
            except Exception as e:
                pass

        if self.md:
            res = self.md.convert(file_path)
            return {
                "filename": name,
                "extension": ".msg",
                "markdown": res.text_content,
                "type": "email"
            }
        
        raise RuntimeError("Nao foi possivel processar o arquivo .msg. Instale extract-msg.")

    def _convert_data_format(self, file_path: str, name: str, ext: str) -> Dict[str, Any]:
        """Formats CSV, JSON, or XML into formatted Markdown tables or syntax-highlighted blocks."""
        if self.md:
            try:
                res = self.md.convert(file_path)
                if res and res.text_content and res.text_content.strip():
                    return {
                        "filename": name,
                        "extension": ext,
                        "markdown": res.text_content,
                        "type": "data"
                    }
            except Exception:
                pass

        with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
            raw_content = f.read()

        if ext == ".csv":
            lines = raw_content.splitlines()
            if lines:
                reader = csv.reader(lines)
                rows = list(reader)
                if rows:
                    header = rows[0]
                    md_table = [
                        "| " + " | ".join(header) + " |",
                        "| " + " | ".join(["---"] * len(header)) + " |"
                    ]
                    for row in rows[1:]:
                        md_table.append("| " + " | ".join(row) + " |")
                    return {
                        "filename": name,
                        "extension": ext,
                        "markdown": f"# Dados CSV: `{name}`\n\n" + "\n".join(md_table),
                        "type": "data"
                    }

        elif ext == ".json":
            try:
                parsed = json.loads(raw_content)
                formatted = json.dumps(parsed, indent=2, ensure_ascii=False)
                return {
                    "filename": name,
                    "extension": ext,
                    "markdown": f"# Dados JSON: `{name}`\n\n```json\n{formatted}\n```",
                    "type": "data"
                }
            except Exception:
                pass

        return {
            "filename": name,
            "extension": ext,
            "markdown": f"# Arquivo `{name}`\n\n```{ext[1:]}\n{raw_content}\n```",
            "type": "data"
        }

    def _fallback_file_convert(self, file_path: str, name: str, ext: str, error_msg: str) -> Dict[str, Any]:
        try:
            with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
                content = f.read()
            return {
                "filename": name,
                "extension": ext,
                "markdown": f"# `{name}`\n\n```\n{content}\n```",
                "type": "file"
            }
        except Exception:
            raise RuntimeError(f"Erro ao converter {name}: {error_msg}")

    def convert_url(self, url: str, use_llm: bool = True) -> Dict[str, Any]:
        """Converts web content (Web HTML, YouTube URL, RSS feed, Wikipedia page) to Markdown."""
        url = url.strip()

        if self.tracker:
            self.tracker.reset()

        result = None
        if "youtube.com" in url or "youtu.be" in url:
            result = self._convert_youtube_url(url)
        elif "wikipedia.org" in url:
            result = self._convert_wikipedia_url(url)
        elif self._is_rss_feed(url):
            result = self._convert_rss_feed(url)
        else:
            if self.md:
                try:
                    res = self.md.convert(url)
                    result = {
                        "url": url,
                        "title": url,
                        "markdown": res.text_content,
                        "type": "web"
                    }
                except Exception:
                    pass

            if result is None:
                try:
                    resp = requests.get(url, timeout=15, headers={"User-Agent": "Mozilla/5.0 (MarkItDownStudio/1.0)"})
                    resp.raise_for_status()
                    soup = BeautifulSoup(resp.text, 'html.parser')
                    
                    title = soup.title.string.strip() if soup.title else url
                    for script in soup(["script", "style", "nav", "footer", "header"]):
                        script.decompose()

                    text = soup.get_text(separator="\n\n")
                    lines = [line.strip() for line in text.splitlines() if line.strip()]
                    clean_text = "\n\n".join(lines)

                    md = f"# {title}\n\n**Fonte:** [{url}]({url})\n\n---\n\n{clean_text}"
                    result = {
                        "url": url,
                        "title": title,
                        "markdown": md,
                        "type": "web"
                    }
                except Exception as e:
                    raise RuntimeError(f"Erro ao carregar URL {url}: {e}")

        if use_llm and self.llm_client is not None and result and result.get("markdown"):
            result["markdown"] = self.refine_markdown_with_llm(result["markdown"], result.get("title", url), ".html")

        llm_used = self.tracker.was_called if (use_llm and self.tracker) else False
        result["llm_used"] = llm_used
        result["llm_model"] = self.llm_model if llm_used else None
        result["llm_provider"] = (self.openai_base_url or "https://api.openai.com/v1") if llm_used else None
        result["llm_calls_count"] = self.tracker.call_count if (llm_used and self.tracker) else 0
        return result

    def _convert_youtube_url(self, url: str) -> Dict[str, Any]:
        """Extracts transcript and metadata from YouTube URL."""
        video_id = None
        if "youtu.be/" in url:
            video_id = url.split("youtu.be/")[1].split("?")[0]
        elif "watch?v=" in url:
            video_id = url.split("watch?v=")[1].split("&")[0]

        md_parts = [f"# Video do YouTube\n\n**URL:** [{url}]({url})\n"]

        if self.md:
            try:
                res = self.md.convert(url)
                if res and hasattr(res, "text_content") and res.text_content.strip():
                    return {
                        "url": url,
                        "title": f"YouTube Video ({video_id or url})",
                        "markdown": res.text_content,
                        "type": "youtube"
                    }
            except Exception:
                pass

        if video_id and YouTubeTranscriptApi is not None:
            try:
                transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=['pt', 'en', 'es'])
                md_parts.append("## Transcricao do Video\n")
                for entry in transcript_list:
                    start_sec = int(entry.get('start', 0))
                    minutes, seconds = divmod(start_sec, 60)
                    timestamp = f"{minutes:02d}:{seconds:02d}"
                    text = entry.get('text', '')
                    md_parts.append(f"`[{timestamp}]` {text}")

                full_md = "\n\n".join(md_parts)
                return {
                    "url": url,
                    "title": f"Transcricao YouTube [{video_id}]",
                    "markdown": full_md,
                    "type": "youtube"
                }
            except Exception as err:
                md_parts.append(f"*(Nao foi possivel extrair transcricao automatica: {err})*")

        md_parts.append(f"\nAssista diretamente em: [{url}]({url})")
        return {
            "url": url,
            "title": f"YouTube Video [{video_id or url}]",
            "markdown": "\n".join(md_parts),
            "type": "youtube"
        }

    def _convert_wikipedia_url(self, url: str) -> Dict[str, Any]:
        """Extracts content from Wikipedia pages."""
        page_title = url.split("/wiki/")[-1] if "/wiki/" in url else url
        page_title = requests.utils.unquote(page_title).replace("_", " ")

        if wikipediaapi is not None:
            try:
                wiki_wiki = wikipediaapi.Wikipedia(user_agent='MarkItDownStudio/1.0', language='pt')
                page = wiki_wiki.page(page_title)
                if not page.exists():
                    wiki_wiki = wikipediaapi.Wikipedia(user_agent='MarkItDownStudio/1.0', language='en')
                    page = wiki_wiki.page(page_title)

                if page.exists():
                    md = f"# Wikipedia: {page.title}\n\n**Origem:** [{url}]({url})\n\n"
                    md += f"## Resumo\n\n{page.summary}\n\n---\n\n"
                    
                    def add_sections(sections, level=2):
                        sec_md = ""
                        for s in sections:
                            sec_md += f"{'#' * level} {s.title}\n\n{s.text}\n\n"
                            sec_md += add_sections(s.sections, level + 1)
                        return sec_md

                    md += add_sections(page.sections)
                    return {
                        "url": url,
                        "title": f"Wikipedia: {page.title}",
                        "markdown": md,
                        "type": "wikipedia"
                    }
            except Exception:
                pass

        if self.md:
            res = self.md.convert(url)
            return {
                "url": url,
                "title": f"Wikipedia: {page_title}",
                "markdown": res.text_content,
                "type": "wikipedia"
            }

        return self.convert_url(url)

    def _is_rss_feed(self, url: str) -> bool:
        return "rss" in url.lower() or "feed" in url.lower() or url.endswith(".xml")

    def _convert_rss_feed(self, url: str) -> Dict[str, Any]:
        """Parses RSS / Atom feeds into Markdown summary."""
        if feedparser is not None:
            try:
                feed = feedparser.parse(url)
                feed_title = feed.feed.get('title', 'Feed RSS')
                feed_desc = feed.feed.get('description', '')

                md = [f"# Feed RSS: {feed_title}\n", f"**URL Feed:** [{url}]({url})\n", f"*{feed_desc}*\n\n---\n"]
                md.append("## Artigos Recentes\n")

                for entry in feed.entries[:20]:
                    title = entry.get('title', 'Sem titulo')
                    link = entry.get('link', '#')
                    published = entry.get('published', entry.get('updated', ''))
                    summary = entry.get('summary', entry.get('description', ''))
                    
                    if summary:
                        summary_soup = BeautifulSoup(summary, 'html.parser')
                        summary_text = summary_soup.get_text()
                    else:
                        summary_text = ""

                    md.append(f"### [{title}]({link})")
                    if published:
                        md.append(f"*Publicado em: {published}*")
                    md.append(f"\n{summary_text[:500]}...\n")
                    md.append("---\n")

                return {
                    "url": url,
                    "title": feed_title,
                    "markdown": "\n".join(md),
                    "type": "rss"
                }
            except Exception as e:
                pass

        return self.convert_url(url)
