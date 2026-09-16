<div align="center">

# 🚀 MarkItDown Studio IDE (简体中文)

**AI 赋能的现代化通用文档转 Markdown 工作站**

[![CI Status](https://github.com/gugaucb/markdown-studio-ide/actions/workflows/ci.yml/badge.svg)](https://github.com/gugaucb/markdown-studio-ide/actions)
[![Docker Image](https://img.shields.io/badge/docker-gugaucb%2Fmarkdown--studio--ide-blue?logo=docker)](https://hub.docker.com/r/gugaucb/markdown-studio-ide)
[![Version](https://img.shields.io/badge/version-1.0.0-green.svg)](https://github.com/gugaucb/markdown-studio-ide/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![i18n](https://img.shields.io/badge/i18n-EN%20%7C%20PT--BR%20%7C%20ZH--CN-orange)](ui/locales/)

[English](README.md) • [Português do Brasil](README.pt-BR.md) • [简体中文](README.zh-CN.md)

<br/>

![MarkItDown Studio IDE 预览](docs/screenshots/app_preview.png)

</div>

---

## 🌟 项目简介

**MarkItDown Studio IDE** 是一款现代、高效的 Web 与桌面端文档格式转换工作区，旨在将各种复杂的电子文档、多媒体流、压缩包以及网页快速转换为**规范、整洁的高质量 Markdown**。

项目基于微软的 `markitdown` 引擎与 `pymupdf4llm` 进行深度封装，提供实时分屏工作区（源码编辑 + HTML 渲染预览）、自动乱码与编码修复管道、严格的表格结构保护机制，并原生支持本地大模型 (Ollama / LM Studio) 及云端提供商 (OpenAI / Groq / OpenRouter)。

---

## ✨ 核心特性

- 📑 **全格式文档支持**：PDF, Word, PowerPoint, Excel, CSV, JSON, XML, 音频, 图像, EPUB, ZIP 以及 Outlook `.msg` 邮件。
- 🌐 **网络内容一键抓取**：直接解析 HTML 网页、YouTube 视频字幕转写、维基百科全文章节以及 RSS 订阅源。
- 🧠 **智能编码与乱码修复**：内置系统级大模型 Prompt，针对字符编码异常（如 UTF-8/Latin-1 乱码）、断行连字符错位进行精准修复。
- 📊 **表格完整度严格保留**：原生提取复杂排版表格为规范 Markdown 表格，杜绝丢失列、合并断层或退化为纯文本。
- 🌍 **多语言原生支持 (i18n)**：支持**英文 (默认)**、**巴西葡萄牙语**与**简体中文**，在导航栏即时切换，浏览器自动保存状态。
- 💻 **双栏分屏 IDE 界面**：具备行号显示、实时文档字数/行数统计、AI 优化徽标提示及实时交互式控制台。
- 🐳 **开箱即用的 Docker 支持**：单命令完成容器化启动，内置与宿主机 Ollama 通信的网关桥接。
- 🧪 **测试驱动开发 (TDD)**：提供完整的 Pytest 测试集与 GitHub Actions 自动化持续集成流程。

---

## 🚀 快速开始

### 1. 使用 Docker 运行 (推荐)

```bash
git clone git@github.com:gugaucb/markdown-studio-ide.git
cd markdown-studio-ide

docker compose up -d
```

打开浏览器访问 **[http://localhost:8000](http://localhost:8000)**。

---

### 2. 本地 Python 环境运行

```bash
git clone git@github.com:gugaucb/markdown-studio-ide.git
cd markdown-studio-ide

# 创建并激活虚拟环境
python -m venv venv
.\venv\Scripts\activate   # Windows
# source venv/bin/activate # Linux/macOS

# 安装依赖
pip install -r requirements.txt

# 启动服务器
python app.py
```

---

## 📄 开源许可

本项目依据 **MIT 许可证** 开源 - 详细内容请参阅 [LICENSE](LICENSE) 文件。
