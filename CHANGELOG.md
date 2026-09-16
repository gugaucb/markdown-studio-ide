# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-09-16

### Added
- **Core Conversion Engine**: Multi-format document conversion powered by `markitdown[all]` and `pymupdf4llm` (PDF, Word, Excel, PowerPoint, CSV, JSON, XML, EPUB, ZIP, Outlook MSG).
- **Web & Media Ingestion**: Direct extraction and formatting for Web HTML pages, YouTube video transcripts, Wikipedia articles, and RSS/Atom feeds.
- **LLM Refinement & Encoding Correction**: Universal AI post-processing prompt for character restoration, mojibake repair (`Ã§Ã£o` -> `ação`), line break defragmentation, and strict table structure preservation.
- **Internationalization (i18n)**: Tri-lingual interface and documentation:
  - English (`en-US`) - Default
  - Brazilian Portuguese (`pt-BR`)
  - Simplified Chinese (`zh-CN`)
  - Instant in-app language switching with `localStorage` persistence.
- **Desktop & Web Studio UI**: Split-view IDE featuring live Markdown editing, syntax-highlighted HTML preview, line numbers, document telemetry counters, category filters, and an activity log console.
- **Automated Test Suite**: Pytest configuration with comprehensive unit and API integration test suites enabling strict Test-Driven Development (TDD).
- **Containerization**: Multi-platform `Dockerfile` and `docker-compose.yml` with host-gateway connectivity for local Ollama instances (`host.docker.internal`).
- **CI/CD Pipelines**: GitHub Actions workflows for automated multi-python testing (`ci.yml`) and automated release publishing to DockerHub (`docker-publish.yml`).
- **Open Source Governance**: Community standards including `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md`, and issue/pull request templates.
