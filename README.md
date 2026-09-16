<div align="center">

# 🚀 MarkItDown Studio IDE

**The Universal, AI-Powered Document-to-Markdown Transformation Studio**

[![CI Status](https://github.com/gugaucb/markdown-studio-ide/actions/workflows/ci.yml/badge.svg)](https://github.com/gugaucb/markdown-studio-ide/actions)
[![Docker Image](https://img.shields.io/badge/docker-gugaucb%2Fmarkdown--studio--ide-blue?logo=docker)](https://hub.docker.com/r/gugaucb/markdown-studio-ide)
[![Version](https://img.shields.io/badge/version-1.1.0-green.svg)](https://github.com/gugaucb/markdown-studio-ide/releases)
[![Python Version](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.13-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![i18n](https://img.shields.io/badge/i18n-EN%20%7C%20PT--BR%20%7C%20ZH--CN-orange)](ui/locales/)

[English](README.md) • [Português do Brasil](README.pt-BR.md) • [简体中文](README.zh-CN.md)

<br/>

![MarkItDown Studio IDE Preview](docs/screenshots/app_preview.png)

</div>

---

## 🌟 Overview

**MarkItDown Studio IDE** is a modern, high-performance web and desktop studio designed to convert any complex document, multimedia stream, archive, or webpage into **pristine, structured Markdown**.

Built on top of Microsoft's `markitdown` and `pymupdf4llm`, it introduces an interactive dual-pane workspace (live code editor + real-time HTML preview), an automated encoding repair pipeline, robust table preservation safeguards, and native support for local (Ollama / LM Studio) and cloud (OpenAI / OpenRouter / Groq) Large Language Models.

---

## ✨ Key Features

- 📑 **Comprehensive Format Coverage**: Convert PDFs, Word, PowerPoint, Excel, CSV, JSON, XML, Audio, Images, EPUB, ZIP, and Outlook `.msg` emails.
- 🌐 **Web & Stream Ingestion**: Extract clean Markdown directly from HTML URLs, YouTube video transcripts (with timestamps), Wikipedia articles, and RSS feeds.
- 🧠 **Encoding & Mojibake Repair**: Built-in intelligent prompt repairing broken UTF-8/ISO encoding anomalies (e.g., `Ã§Ã£o` -> `ação`), stitching hyphenated line-breaks, and restoring document orthography.
- 📊 **Strict Table Preservation**: High-fidelity conversion retaining Markdown table layout and cell data without summary truncation.
- 🌍 **Full Tri-Lingual i18n**: Out-of-the-box support for **English (Default)**, **Português (Brasil)**, and **简体中文**, switchable on the fly with `localStorage` persistence.
- 💻 **Dual-Pane IDE Workspace**: Split-view editor with line numbering, document metrics (characters, words, lines, AI badges), and live activity console.
- 🐳 **Docker & DockerHub Ready**: Single-command container deployment with automated gateway bridge to host-based Ollama models.
- 🧪 **TDD & CI/CD**: 100% automated test coverage with Pytest and GitHub Actions workflows.

---

## 📁 Supported Formats & Engines

| Category | Extensions / Sources | Extraction Capabilities |
| :--- | :--- | :--- |
| **Documents** | `.pdf`, `.docx`, `.pptx`, `.xlsx`, `.xls` | PyMuPDF4LLM table layout, slide-by-slide hierarchy, sheets |
| **Data** | `.csv`, `.json`, `.xml` | Formatted interactive tables, formatted syntax-highlighted blocks |
| **Web & Feeds** | HTML URLs, Wikipedia, RSS / Atom | Main content isolation, article digests, section trees |
| **Multimedia** | YouTube URLs, `.mp3`, `.wav`, `.m4a` | Speech-to-text transcriptions with timestamps |
| **Images** | `.png`, `.jpg`, `.jpeg`, `.webp`, `.bmp` | Vision OCR & multimodal image understanding (with LLM) |
| **Archives & Books**| `.zip`, `.epub` | Recursive unpacking with linked markdown table of contents |
| **Emails** | `.msg` | Header extraction (From, To, Date, Subject) and email body |

---

## 🚀 Quick Start

### 1. Run with Docker (Recommended)

```bash
# Clone the repository
git clone git@github.com:gugaucb/markdown-studio-ide.git
cd markdown-studio-ide

# Start with Docker Compose
docker compose up -d
```

Open your browser at **[http://localhost:8000](http://localhost:8000)**.

> **Note:** The Docker container automatically connects to local Ollama running on your host machine via `host.docker.internal:11434`.

---

### 2. Run Locally with Python

```bash
# Clone the repository
git clone git@github.com:gugaucb/markdown-studio-ide.git
cd markdown-studio-ide

# Create and activate virtual environment
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start the IDE server
python app.py
```

Access the studio at **`http://127.0.0.1:8000`**.

---

## 🤖 Local & Cloud AI Configuration

Click the **Gear Icon (<i class="fa-solid fa-gear"></i>)** in the top navigation bar to configure your AI provider:

- **Local Ollama (Recommended & Free):**
  - Base URL: `http://127.0.0.1:11434/v1`
  - Model: `gemma4:26b`, `llama3.3:70b`, `llama3.2-vision`, `qwen2.5:7b`
  - API Key: Leave empty.
- **OpenAI:**
  - Base URL: `https://api.openai.com/v1`
  - Model: `gpt-4o`, `gpt-4o-mini`
  - API Key: `sk-proj-...`
- **Groq / OpenRouter / LM Studio:**
  - Enter the compatible endpoint URL, model identifier, and key.

---

## 🧪 Running Tests (TDD)

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run pytest test suite
pytest
```

---

## 🗺️ Roadmap & Community

- [x] Multi-format conversion core (`markitdown`, `pymupdf4llm`)
- [x] Universal encoding and mojibake correction prompt
- [x] Tri-lingual i18n (`en-US`, `pt-BR`, `zh-CN`)
- [x] Pytest automated test suites (TDD)
- [x] Docker & Docker Compose setup
- [x] GitHub Actions CI & DockerHub workflows
- [x] SemVer release `v1.0.0`
- [x] Desktop packaging (native installers for Windows `.exe` / macOS `.dmg` via PyWebView)
- [ ] Batch folder watch daemon

---

## 🤝 Contributing

Contributions are warmly welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) and review our [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) before submitting Pull Requests.

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.
