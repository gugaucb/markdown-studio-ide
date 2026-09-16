# MarkItDown Studio IDE - End User Guide

Welcome to the comprehensive user guide for **MarkItDown Studio IDE**. This manual walks you through all document conversion modes, LLM configuration options, and export workflows.

---

## 📑 Table of Contents

1. [Interface Tour](#interface-tour)
2. [Converting Local Files](#converting-local-files)
3. [Converting Web URLs & Streaming Media](#converting-web-urls--streaming-media)
4. [AI Refinement & Encoding Correction](#ai-refinement--encoding-correction)
5. [Configuring LLM Providers](#configuring-llm-providers)
6. [Exporting & Saving Your Work](#exporting--saving-your-work)
7. [Language & Localization](#language--localization)
8. [Troubleshooting & FAQs](#troubleshooting--faqs)

---

## 1. Interface Tour

The studio is organized into three primary operational areas:

- **Top Navbar:**
  - **Status Pill:** Indicates whether AI refinement is connected, active, or idle.
  - **Use AI Toggle:** Instantly switches AI post-processing on/off for faster or enriched conversion.
  - **Convert URL Button:** Opens the web ingestion dialog.
  - **Open Files Button:** Triggers native OS file picker.
  - **Gear Settings:** Opens LLM endpoint configuration.
  - **Language Selector:** Switch between English (`EN`), Portuguese (`PT`), and Chinese (`中文`).
- **Left Sidebar:**
  - **Category Filters:** Filter converted documents by `All`, `Docs`, `Web/YT`, `Data`, `Media`, `Zip/eBook`, or `Email/RSS`.
  - **Drop Zone:** Interactive area to drag and drop single or multiple files.
  - **Document Tree:** Hierarchical list of all currently converted files in memory.
- **Center Workspace:**
  - **Tab Bar:** Switch between opened documents.
  - **View Modes:** Toggle between `Split` (side-by-side), `Editor` (raw markdown only), or `Preview` (rendered HTML only).
  - **Metrics Bar:** Real-time counters showing characters, words, lines, and AI model badge.
  - **Bottom Terminal:** Collapsible console displaying system activity, conversion logs, and HTTP statuses.

---

## 2. Converting Local Files

### Drag-and-Drop
Simply drag one or more files from your file manager (Windows Explorer, macOS Finder, or Linux Files) and drop them into the dashed **Drop Zone** on the left panel.

### File Selector Dialog
Click the **"Open Files"** button in the header or the link inside the drop zone to open the system file chooser.

### Supported File Types:
- **Office Documents:** `.docx`, `.pptx`, `.xlsx`, `.xls`
- **PDFs:** Standard `.pdf` files are parsed using `pymupdf4llm` to preserve tables.
- **Data Sets:** `.csv`, `.json`, `.xml`
- **Images (with OCR):** `.png`, `.jpg`, `.jpeg`, `.webp`, `.bmp`
- **Audio (Speech-to-Text):** `.mp3`, `.wav`, `.m4a`
- **Archives & Books:** `.zip` (extracts all sub-files and generates an index), `.epub`
- **Outlook Emails:** `.msg` (extracts headers and email body)

---

## 3. Converting Web URLs & Streaming Media

Click the **"Convert URL"** button in the top navigation bar:

1. **YouTube Videos:**
   - Input format: `https://www.youtube.com/watch?v=...` or `https://youtu.be/...`
   - Output: Formatted video metadata, link, and the full transcript with timestamps.
2. **Wikipedia Articles:**
   - Input format: `https://en.wikipedia.org/wiki/...`
   - Output: Title, summary, and hierarchical sections (`## Heading 2`, `### Heading 3`).
3. **RSS / Atom Feeds:**
   - Input format: `https://example.com/feed.xml` or `https://example.com/rss`
   - Output: Channel title, description, and list of the latest articles with hyperlinks and publication dates.
4. **General Webpages (HTML):**
   - Strips ads, scripts, navbars, and footers, extracting the core readable article content in Markdown.

---

## 4. AI Refinement & Encoding Correction

When the **"Use AI"** toggle is enabled, MarkItDown Studio IDE applies a post-processing pass using your configured LLM:

- **Encoding Anomaly Repair (Mojibake):** Detects character scrambling (such as `Ã§Ã£o` instead of `ação`) and fixes them according to the document's original language.
- **Word Reassembly:** Joins words split across page breaks or broken by PDF line-wrapping.
- **Table Preservation:** Markdown table headers (`| Col1 | Col2 |`) are strictly preserved. If an LLM response accidentally omits a table, the built-in safeguard automatically protects and restores the original table intact.

---

## 5. Configuring LLM Providers

Click the **Gear (<i class="fa-solid fa-gear"></i>)** icon in the navbar:

### Option A: Local Ollama (Free, Private, Offline)
1. Install and run [Ollama](https://ollama.com).
2. Download a recommended model: `ollama pull gemma4:26b` or `ollama pull llama3.2`
3. In the Settings modal:
   - **Base URL:** `http://127.0.0.1:11434/v1`
   - **API Key:** Leave empty.
   - **Model:** `gemma4:26b` (or your chosen model).
4. Click **"Test Connection"** to verify, then click **"Save Settings"**.

### Option B: OpenAI Official
1. Obtain an API key from [platform.openai.com](https://platform.openai.com).
2. In the Settings modal:
   - **Base URL:** `https://api.openai.com/v1`
   - **API Key:** `sk-proj-...`
   - **Model:** `gpt-4o` or `gpt-4o-mini`
3. Click **"Save Settings"**.

---

## 6. Exporting & Saving Your Work

Inside the workspace toolbar:
- **Copy:** Copies the active raw Markdown directly to your OS clipboard.
- **Download:** Downloads the `.md` file to your browser's default Downloads folder.
- **Export .md:** Saves the file directly into the server's local `exports/` folder.
- **HTML:** Generates a standalone, styled `.html` file for offline presentation or printing.

---

## 7. Language & Localization

The user interface supports three languages:
- **English (`EN`)** - Default
- **Português (`PT`)**
- **简体中文 (`中文`)**

Click any of the language buttons in the top navbar. The entire UI updates instantly without reloading the page, and your selection is saved for future sessions.
