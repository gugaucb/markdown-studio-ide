/**
 * MarkItDown Studio IDE - Internationalization (i18n) Engine
 * Supported Locales:
 * - en-US (English - Default)
 * - pt-BR (Português do Brasil)
 * - zh-CN (简体中文)
 */

const I18N_TRANSLATIONS = {
  "en-US": {
    "app_title": "MarkItDown Studio IDE - Universal Markdown Transformer",
    "version": "v1.0",
    "llm_disabled": "AI Disabled (No Key/Endpoint)",
    "llm_enabled": "AI Active ({model})",
    "use_ai": "Use AI",
    "use_ai_hint": "Enable/disable AI (Ollama / OpenAI) for conversion, table preservation, and document refinement",
    "convert_url": "Convert URL",
    "convert_url_hint": "Convert Web URL (YouTube, Wikipedia, RSS, HTML)",
    "open_files": "Open Files",
    "open_files_hint": "Convert Local Documents",
    "settings_title": "Settings & API Configuration",
    "explorer": "Explorer",
    "clear_queue": "Clear Queue",
    "filter_all": "All",
    "filter_docs": "Docs",
    "filter_web": "Web/YT",
    "filter_data": "Data",
    "filter_media": "Media",
    "filter_archive": "Zip/eBook",
    "filter_other": "Email/RSS",
    "drop_text": "Drag and drop files here or <span class=\"browse-link\">browse to upload</span>",
    "drop_hint": "PDF, DOCX, PPTX, XLSX, CSV, JSON, XML, PNG, MP3, EPUB, ZIP, MSG",
    "converted_docs": "Converted Documents ({count})",
    "no_files_converted": "No documents converted yet",
    "split_view": "Split",
    "editor_only": "Editor",
    "preview_only": "Preview",
    "metric_chars": "chars",
    "metric_words": "words",
    "metric_lines": "lines",
    "metric_ai_processed": "AI Refined",
    "copy_markdown": "Copy",
    "copied": "Copied!",
    "download_browser": "Download",
    "export_local": "Export .md",
    "export_html": "HTML",
    "processing_title": "Processing Document...",
    "processing_subtitle": "Converting and refining structure with AI ({model})...",
    "editor_header": "Markdown Editor",
    "editor_placeholder": "Select or convert a document to view and edit its Markdown...",
    "preview_header": "Real-time Rendered Preview",
    "terminal_title": "Conversion & Activity Console",
    "terminal_clear": "Clear Console",
    "terminal_toggle": "Minimize/Expand Console",
    "terminal_ready": "[SYSTEM] MarkItDown Studio IDE initialized. Waiting for files or URLs...",
    "modal_url_title": "Convert Web URL or Media Stream",
    "modal_url_label": "Paste target URL:",
    "modal_url_placeholder": "https://youtube.com/watch?v=... or Wikipedia or RSS Feed...",
    "hint_youtube": "YouTube (Transcript)",
    "hint_wikipedia": "Wikipedia",
    "hint_rss": "RSS Feed",
    "hint_html": "HTML Webpage",
    "btn_cancel": "Cancel",
    "btn_convert_url": "Convert to Markdown",
    "modal_settings_title": "AI Provider & Model Settings",
    "modal_settings_desc": "Configure your OpenAI-compatible endpoint (Ollama, LM Studio, OpenAI, OpenRouter, Groq, DeepSeek) for intelligent character repair, OCR, and document structure enrichment.",
    "settings_url_label": "OpenAI-compatible Base URL (Optional):",
    "settings_url_placeholder": "Default: https://api.openai.com/v1 (or http://127.0.0.1:11434/v1)",
    "settings_key_label": "API Key (sk-... or leave empty for local Ollama):",
    "settings_key_placeholder": "sk-proj-... (or blank for local Ollama)",
    "settings_model_label": "AI Model / Vision Engine:",
    "btn_test_conn": "Test Connection",
    "btn_save_settings": "Save Settings",
    "welcome_tab": "Welcome.md",
    "exported_success": "Saved successfully to exports directory!",
    "saved_path": "File saved at: {path}",
    "error_occurred": "Error: {error}"
  },
  "pt-BR": {
    "app_title": "MarkItDown Studio IDE - Transformador Universal para Markdown",
    "version": "v1.0",
    "llm_disabled": "IA Desativada (Sem Key)",
    "llm_enabled": "IA Ativa ({model})",
    "use_ai": "Usar IA",
    "use_ai_hint": "Ativar/desativar uso de IA (gemma4:26b / Ollama) na conversão e enriquecimento dos documentos",
    "convert_url": "Converter URL",
    "convert_url_hint": "Converter URL (YouTube, Wikipedia, RSS, HTML)",
    "open_files": "Abrir Arquivos",
    "open_files_hint": "Converter Arquivos Locais",
    "settings_title": "Configurações & API Key",
    "explorer": "Explorador",
    "clear_queue": "Limpar Lista",
    "filter_all": "Todos",
    "filter_docs": "Docs",
    "filter_web": "Web/YT",
    "filter_data": "Dados",
    "filter_media": "Mídia",
    "filter_archive": "Zip/eBook",
    "filter_other": "Email/RSS",
    "drop_text": "Arraste arquivos aqui ou <span class=\"browse-link\">clique para selecionar</span>",
    "drop_hint": "PDF, DOCX, PPTX, XLSX, CSV, JSON, XML, PNG, MP3, EPUB, ZIP, MSG",
    "converted_docs": "Documentos Convertidos ({count})",
    "no_files_converted": "Nenhum arquivo convertido ainda",
    "split_view": "Split",
    "editor_only": "Editor",
    "preview_only": "Preview",
    "metric_chars": "caracteres",
    "metric_words": "palavras",
    "metric_lines": "linhas",
    "metric_ai_processed": "Refinado com IA",
    "copy_markdown": "Copiar",
    "copied": "Copiado!",
    "download_browser": "Download",
    "export_local": "Exportar .md",
    "export_html": "HTML",
    "processing_title": "Processando documento...",
    "processing_subtitle": "Convertendo e refinando com IA ({model})...",
    "editor_header": "Editor Markdown",
    "editor_placeholder": "Selecione ou converta um documento para editar seu código Markdown...",
    "preview_header": "Renderização em Tempo Real",
    "terminal_title": "Console de Conversão & Logs",
    "terminal_clear": "Limpar Logs",
    "terminal_toggle": "Minimizar/Expandir Terminal",
    "terminal_ready": "[SISTEMA] MarkItDown Studio IDE iniciado com sucesso. Aguardando arquivos ou URLs...",
    "modal_url_title": "Converter URL Web ou Mídia",
    "modal_url_label": "Cole o Link de Destino:",
    "modal_url_placeholder": "https://youtube.com/watch?v=... ou Wikipedia ou RSS Feed...",
    "hint_youtube": "YouTube (Transcrição)",
    "hint_wikipedia": "Wikipedia",
    "hint_rss": "Feed RSS",
    "hint_html": "Página HTML",
    "btn_cancel": "Cancelar",
    "btn_convert_url": "Converter para Markdown",
    "modal_settings_title": "Configurações do Provedor de IA",
    "modal_settings_desc": "Configure seu provedor compatível com o padrão OpenAI (OpenAI, Ollama, OpenRouter, Groq, LM Studio, etc.) para habilitar OCR inteligente, correção de encode e refinamento de tabelas.",
    "settings_url_label": "URL da API OpenAI-compatível (Opcional):",
    "settings_url_placeholder": "Padrão: https://api.openai.com/v1 (ou http://127.0.0.1:11434/v1)",
    "settings_key_label": "Chave da API (sk-... ou vazia p/ Ollama local):",
    "settings_key_placeholder": "sk-proj-... (ou deixe vazio para Ollama local)",
    "settings_model_label": "Modelo de IA / Multimodal:",
    "btn_test_conn": "Testar Conexão",
    "btn_save_settings": "Salvar Configurações",
    "welcome_tab": "Bem-vindo.md",
    "exported_success": "Arquivo exportado com sucesso para a pasta exports/!",
    "saved_path": "Salvo em: {path}",
    "error_occurred": "Erro: {error}"
  },
  "zh-CN": {
    "app_title": "MarkItDown Studio IDE - 通用 Markdown 转换工具",
    "version": "v1.0",
    "llm_disabled": "AI 已禁用 (未配置密钥/终端)",
    "llm_enabled": "AI 运行中 ({model})",
    "use_ai": "启用 AI",
    "use_ai_hint": "启用/禁用 AI (Ollama / OpenAI) 进行文档转换、结构优化和表格保持",
    "convert_url": "转换 URL",
    "convert_url_hint": "转换网络链接 (YouTube, 维基百科, RSS, HTML)",
    "open_files": "打开文件",
    "open_files_hint": "转换本地文档",
    "settings_title": "设置与 API 配置",
    "explorer": "资源管理器",
    "clear_queue": "清空列表",
    "filter_all": "全部",
    "filter_docs": "文档",
    "filter_web": "网页/视频",
    "filter_data": "数据",
    "filter_media": "媒体",
    "filter_archive": "压缩包/电子书",
    "filter_other": "邮件/RSS",
    "drop_text": "将文件拖拽至此处，或 <span class=\"browse-link\">点击选择文件</span>",
    "drop_hint": "支持 PDF, DOCX, PPTX, XLSX, CSV, JSON, XML, PNG, MP3, EPUB, ZIP, MSG",
    "converted_docs": "已转换文档 ({count})",
    "no_files_converted": "暂无已转换的文件",
    "split_view": "分屏",
    "editor_only": "编辑器",
    "preview_only": "预览",
    "metric_chars": "字符",
    "metric_words": "单词",
    "metric_lines": "行数",
    "metric_ai_processed": "AI 优化",
    "copy_markdown": "复制",
    "copied": "已复制!",
    "download_browser": "下载",
    "export_local": "导出 .md",
    "export_html": "HTML",
    "processing_title": "正在处理文档...",
    "processing_subtitle": "正在使用 AI ({model}) 进行转换与编码修复...",
    "editor_header": "Markdown 编辑器",
    "editor_placeholder": "请选择或转换文档以查看并编辑其 Markdown 代码...",
    "preview_header": "实时渲染预览",
    "terminal_title": "转换控制台与日志",
    "terminal_clear": "清空日志",
    "terminal_toggle": "最小化/展开控制台",
    "terminal_ready": "[系统] MarkItDown Studio IDE 已就绪。等待文件或 URL...",
    "modal_url_title": "转换网络 URL 或流媒体",
    "modal_url_label": "粘贴目标网址：",
    "modal_url_placeholder": "https://youtube.com/watch?v=... 或 Wikipedia 或 RSS 订阅源...",
    "hint_youtube": "YouTube (字幕转写)",
    "hint_wikipedia": "维基百科",
    "hint_rss": "RSS 订阅",
    "hint_html": "HTML 网页",
    "btn_cancel": "取消",
    "btn_convert_url": "开始转换为 Markdown",
    "modal_settings_title": "AI 提供商与模型设置",
    "modal_settings_desc": "配置兼容 OpenAI 标准的服务端点 (Ollama, LM Studio, OpenAI, OpenRouter, Groq, DeepSeek)，用于智能编码修复、OCR 识别与表格结构保留。",
    "settings_url_label": "兼容 OpenAI 的 Base URL (可选)：",
    "settings_url_placeholder": "默认: https://api.openai.com/v1 (或 http://127.0.0.1:11434/v1)",
    "settings_key_label": "API Key (sk-... 或本地 Ollama 留空)：",
    "settings_key_placeholder": "sk-proj-... (本地 Ollama 可留空)",
    "settings_model_label": "AI 模型 / 多模态引擎：",
    "btn_test_conn": "测试连接",
    "btn_save_settings": "保存设置",
    "welcome_tab": "欢迎.md",
    "exported_success": "成功保存到 exports/ 目录！",
    "saved_path": "已保存至: {path}",
    "error_occurred": "错误: {error}"
  }
};

class I18nManager {
  constructor() {
    this.storageKey = "markitdown_app_lang";
    // Default to en-US as explicitly requested
    this.currentLocale = localStorage.getItem(this.storageKey) || "en-US";
    if (!I18N_TRANSLATIONS[this.currentLocale]) {
      this.currentLocale = "en-US";
    }
  }

  t(key, params = {}) {
    const dict = I18N_TRANSLATIONS[this.currentLocale] || I18N_TRANSLATIONS["en-US"];
    let text = dict[key] || (I18N_TRANSLATIONS["en-US"][key] || key);
    for (const [pKey, pVal] of Object.entries(params)) {
      text = text.replace(new RegExp(`\\{${pKey}\\}`, "g"), pVal);
    }
    return text;
  }

  setLanguage(locale) {
    if (!I18N_TRANSLATIONS[locale]) return;
    this.currentLocale = locale;
    localStorage.setItem(this.storageKey, locale);
    this.applyTranslations();
    window.dispatchEvent(new CustomEvent("languageChanged", { detail: { locale } }));
  }

  applyTranslations() {
    document.documentElement.lang = this.currentLocale;
    document.title = this.t("app_title");

    // Elements with data-i18n
    document.querySelectorAll("[data-i18n]").forEach(el => {
      const key = el.getAttribute("data-i18n");
      if (key) {
        el.innerHTML = this.t(key);
      }
    });

    // Elements with data-i18n-title
    document.querySelectorAll("[data-i18n-title]").forEach(el => {
      const key = el.getAttribute("data-i18n-title");
      if (key) {
        el.setAttribute("title", this.t(key));
      }
    });

    // Elements with data-i18n-placeholder
    document.querySelectorAll("[data-i18n-placeholder]").forEach(el => {
      const key = el.getAttribute("data-i18n-placeholder");
      if (key) {
        el.setAttribute("placeholder", this.t(key));
      }
    });

    // Update active state on language buttons
    document.querySelectorAll(".lang-switch-btn").forEach(btn => {
      btn.classList.toggle("active", btn.getAttribute("data-lang") === this.currentLocale);
    });
  }
}

window.i18n = new I18nManager();
