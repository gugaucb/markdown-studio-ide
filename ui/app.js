/**
 * MARKITDOWN STUDIO IDE - FRONTEND LOGIC
 */

document.addEventListener('DOMContentLoaded', () => {
    // --- STATE ---
    let convertedFiles = [];
    let activeTabId = 'welcome';
    let viewMode = 'split'; // 'split' | 'editor' | 'preview'
    let currentCategoryFilter = 'all';
    let logsCount = 0;
    let apiKey = '';
    let llmModel = 'gemma4:26b';
    let apiBaseUrl = 'http://127.0.0.1:11434/v1';
    const STORAGE_KEY_SETTINGS = 'markitdown_settings';
    const STORAGE_KEY_USE_LLM = 'markitdown_use_llm';

    // --- MULTILINGUAL INITIAL WELCOME DOCUMENT ---
    function getWelcomeContent(locale) {
        if (locale === 'pt-BR') {
            return {
                filename: 'Bem-vindo.md',
                title: 'Bem-vindo ao MarkItDown Studio IDE',
                markdown: `# 🚀 Bem-vindo ao MarkItDown Studio IDE\n\nTransforme qualquer formato de documento, mídia, página web, arquivo compactado ou e-mail em **Markdown limpo** usando o poder do \`markitdown[all]\`.\n\n---\n\n## 📁 Extensões e Fontes Suportadas\n\n### 📄 Documentos\n* **PDF** (\`.pdf\`) - Extração de texto e estruturação com preservação de tabelas\n* **Word** (\`.docx\`) - Formatação de títulos, listas e tabelas\n* **PowerPoint** (\`.pptx\`) - Conteúdo por slide\n* **Excel** (\`.xlsx\`, \`.xls\`) - Tabelas Markdown integradas\n\n### 🌐 Conteúdo Web\n* **Páginas HTML** - Conversão direta via Web Fetch\n* **URLs do YouTube** - Extração automática de transcrição com timestamps\n* **Wikipedia** - Artigos estruturados com índice e seções\n* **Feeds RSS** - Digest com lista de artigos recentes\n\n### 📊 Formatos de Dados\n* **CSV** - Tabelas Markdown interativas\n* **JSON** - Blocos de código formatados e estruturados\n* **XML** - Árvore de dados e formatação legível\n\n### 📷 Mídia (com Suporte a IA/Visão)\n* **Imagens** (\`.png\`, \`.jpg\`, \`.jpeg\`, \`.webp\`) - OCR e descrições visuais geradas por IA\n* **Áudio** (\`.mp3\`, \`.wav\`, \`.m4a\`) - Transcrição de voz para texto\n\n### 📚 eBooks & Arquivos\n* **EPUB** (\`.epub\`) - Extração de capítulos\n* **ZIP Archives** (\`.zip\`) - Descompactação recursiva e concatenação com índice\n\n### ✉️ Outros\n* **Mensagens do Outlook** (\`.msg\`) - Cabeçalhos (De, Para, Assunto) e corpo em Markdown\n\n---\n\n## 🛠️ Como Usar\n\n1. **Upload de Arquivos:** Arraste e solte arquivos no painel à esquerda ou clique em **"Abrir Arquivos"**.\n2. **URLs:** Clique em **"Converter URL"** no menu superior para processar links do YouTube, Wikipedia ou RSS.\n3. **Visão Dividida (Split IDE):** Edite o código Markdown no painel esquerdo enquanto visualiza a renderização final em tempo real à direita.\n4. **Exportação:** Copie o resultado para a área de transferência ou exporte como \`.md\` e \`.html\`.\n5. **Visão / Áudio com IA:** Configure sua chave de API ou Ollama local no ícone de engrenagem <i class="fa-solid fa-gear"></i>.\n`
            };
        } else if (locale === 'zh-CN') {
            return {
                filename: '欢迎.md',
                title: '欢迎使用 MarkItDown Studio IDE',
                markdown: `# 🚀 欢迎使用 MarkItDown Studio IDE\n\n借助 \`markitdown[all]\` 的强大功能，将各种文档、多媒体、网页、压缩包或电子邮件转换为**清晰规范的 Markdown**。\n\n---\n\n## 📁 支持的格式与来源\n\n### 📄 文档\n* **PDF** (\`.pdf\`) - 智能文本提取与表格排版保留\n* **Word** (\`.docx\`) - 标题、列表及格式化表格提取\n* **PowerPoint** (\`.pptx\`) - 幻灯片逐页内容提取\n* **Excel** (\`.xlsx\`, \`.xls\`) - 自动转换为 Markdown 规范表格\n\n### 🌐 网络内容\n* **HTML 网页** - 在线抓取与内容提炼\n* **YouTube 链接** - 带时间戳的自动字幕/转写提取\n* **维基百科** - 包含目录与章节的结构化文章\n* **RSS 订阅** - 最新文章摘要整合\n\n### 📊 数据格式\n* **CSV** - 结构化交互式 Markdown 表格\n* **JSON** - 格式化高亮代码块\n* **XML** - 树状数据清晰呈现\n\n### 📷 多媒体 (支持 AI / 视觉模型)\n* **图像** (\`.png\`, \`.jpg\`, \`.jpeg\`, \`.webp\`) - 智能 OCR 与多模态图像解读\n* **音频** (\`.mp3\`, \`.wav\`, \`.m4a\`) - 语音转写为文字\n\n### 📚 电子书与压缩包\n* **EPUB** (\`.epub\`) - 章节解析与内容提取\n* **ZIP 压缩包** (\`.zip\`) - 递归解包合并并生成文件索引\n\n### ✉️ 其他格式\n* **Outlook 邮件** (\`.msg\`) - 邮件头 (发件人、收件人、日期、主题) 与正文转换\n\n---\n\n## 🛠️ 快速上手\n\n1. **上传文件：** 将文件拖拽至左侧面板，或点击 **"打开文件"** 按钮。\n2. **转换网络链接：** 点击顶部菜单的 **"转换 URL"**，处理 YouTube、维基百科或 RSS 源。\n3. **分屏工作区：** 左侧实时编辑 Markdown 源码，右侧即时查看 HTML 渲染预览。\n4. **导出成果：** 一键复制到剪贴板，或直接导出为 \`.md\` 和 \`.html\`。\n5. **本地 AI / 多模态设置：** 点击右上角齿轮设置图标 <i class="fa-solid fa-gear"></i> 配置 Ollama 或 OpenAI。\n`
            };
        } else {
            return {
                filename: 'Welcome.md',
                title: 'Welcome to MarkItDown Studio IDE',
                markdown: `# 🚀 Welcome to MarkItDown Studio IDE\n\nTransform any document format, media file, web page, compressed archive, or email into **clean Markdown** using the power of \`markitdown[all]\`.\n\n---\n\n## 📁 Supported Extensions & Sources\n\n### 📄 Documents\n* **PDF** (\`.pdf\`) - Layout-aware text extraction & table preservation\n* **Word** (\`.docx\`) - Headings, bullet lists, formatting, and tables\n* **PowerPoint** (\`.pptx\`) - Slide-by-slide structure\n* **Excel** (\`.xlsx\`, \`.xls\`) - Converted into native Markdown tables\n\n### 🌐 Web Content\n* **HTML Webpages** - Direct conversion via web fetching\n* **YouTube URLs** - Automatic transcript extraction with timestamps\n* **Wikipedia** - Structured articles with table of contents & sections\n* **RSS Feeds** - Recent article digests\n\n### 📊 Data Formats\n* **CSV** - Clean interactive Markdown tables\n* **JSON** - Formatted syntax-highlighted codeblocks\n* **XML** - Structured data trees\n\n### 📷 Media (with AI / Vision Support)\n* **Images** (\`.png\`, \`.jpg\`, \`.jpeg\`, \`.webp\`) - Smart OCR and multimodal descriptions\n* **Audio** (\`.mp3\`, \`.wav\`, \`.m4a\`) - Speech-to-text transcriptions\n\n### 📚 eBooks & Archives\n* **EPUB** (\`.epub\`) - Chapter-by-chapter extraction\n* **ZIP Archives** (\`.zip\`) - Recursive extraction with concatenated index\n\n### ✉️ Other\n* **Outlook Emails** (\`.msg\`) - Headers (From, To, Date, Subject) and Markdown body\n\n---\n\n## 🛠️ Quick Start\n\n1. **Upload Files:** Drag and drop files onto the left panel or click **"Open Files"**.\n2. **URLs:** Click **"Convert URL"** in the top navbar to process YouTube, Wikipedia, or RSS links.\n3. **Split IDE View:** Edit raw Markdown on the left while previewing live HTML on the right.\n4. **Export:** Copy to clipboard or export directly as \`.md\` or \`.html\`.\n5. **Local AI / Vision:** Configure Ollama or OpenAI settings in the gear icon <i class="fa-solid fa-gear"></i>.\n`
            };
        }
    }

    const currentLang = window.i18n ? window.i18n.currentLocale : 'en-US';
    const initialContent = getWelcomeContent(currentLang);
    const welcomeDoc = {
        id: 'welcome',
        filename: initialContent.filename,
        title: initialContent.title,
        type: 'guide',
        category: 'docs',
        extension: '.md',
        markdown: initialContent.markdown
    };

    convertedFiles.push(welcomeDoc);

    // --- DOM ELEMENTS ---
    const dropZone = document.getElementById('dropZone');
    const fileInput = document.getElementById('fileInput');
    const btnTriggerUpload = document.getElementById('btnTriggerUpload');
    const fileTree = document.getElementById('fileTree');
    const convertedCount = document.getElementById('convertedCount');
    const tabBar = document.getElementById('tabBar');
    const markdownEditor = document.getElementById('markdownEditor');
    const markdownPreview = document.getElementById('markdownPreview');
    const lineNumbers = document.getElementById('lineNumbers');

    const btnSplitView = document.getElementById('btnSplitView');
    const btnEditorOnly = document.getElementById('btnEditorOnly');
    const btnPreviewOnly = document.getElementById('btnPreviewOnly');
    const editorPane = document.getElementById('editorPane');
    const previewPane = document.getElementById('previewPane');

    const metricChars = document.getElementById('metricChars');
    const metricWords = document.getElementById('metricWords');
    const metricLines = document.getElementById('metricLines');
    const metricAiUsage = document.getElementById('metricAiUsage');
    const metricAiModel = document.getElementById('metricAiModel');

    const btnCopyMarkdown = document.getElementById('btnCopyMarkdown');
    const btnExportMd = document.getElementById('btnExportMd');
    const btnExportLocalMd = document.getElementById('btnExportLocalMd');
    const btnExportHtml = document.getElementById('btnExportHtml');

    const terminalConsole = document.getElementById('terminalConsole');
    const bottomTerminal = document.getElementById('bottomTerminal');
    const toggleTerminalBtn = document.getElementById('toggleTerminalBtn');
    const btnMinimizeTerminal = document.getElementById('btnMinimizeTerminal');
    const btnClearLogs = document.getElementById('btnClearLogs');
    const logBadge = document.getElementById('logBadge');

    const urlModal = document.getElementById('urlModal');
    const btnOpenUrlModal = document.getElementById('btnOpenUrlModal');
    const btnCloseUrlModal = document.getElementById('btnCloseUrlModal');
    const btnCancelUrl = document.getElementById('btnCancelUrl');
    const btnSubmitUrl = document.getElementById('btnSubmitUrl');
    const urlInput = document.getElementById('urlInput');

    const settingsModal = document.getElementById('settingsModal');
    const btnOpenSettings = document.getElementById('btnOpenSettings');
    const btnCloseSettingsModal = document.getElementById('btnCloseSettingsModal');
    const btnCancelSettings = document.getElementById('btnCancelSettings');
    const btnSaveSettings = document.getElementById('btnSaveSettings');
    const btnTestSettings = document.getElementById('btnTestSettings');
    const apiBaseUrlInput = document.getElementById('apiBaseUrlInput');
    const apiKeyInput = document.getElementById('apiKeyInput');
    const llmModelInput = document.getElementById('llmModelInput');
    const llmTestFeedback = document.getElementById('llmTestFeedback');
    const llmStatusPill = document.getElementById('llmStatusPill');

    const toggleUseLlm = document.getElementById('toggleUseLlm');
    const processingOverlay = document.getElementById('processingOverlay');
    const spinnerTitle = document.getElementById('spinnerTitle');
    const spinnerSubtitle = document.getElementById('spinnerSubtitle');

    // --- MARKED JS CONFIG ---
    if (typeof marked !== 'undefined') {
        marked.setOptions({
            gfm: true,
            breaks: true,
            highlight: function(code, lang) {
                if (typeof hljs !== 'undefined' && lang && hljs.getLanguage(lang)) {
                    try {
                        return hljs.highlight(code, { language: lang }).value;
                    } catch (e) {}
                }
                return code;
            }
        });
    }

    // --- LOG FUNCTIONS ---
    function log(msg, type = 'info') {
        logsCount++;
        logBadge.textContent = logsCount;
        const entry = document.createElement('div');
        entry.className = `log-entry ${type}`;
        const time = new Date().toLocaleTimeString();
        entry.textContent = `[${time}] ${msg}`;
        terminalConsole.appendChild(entry);
        terminalConsole.scrollTop = terminalConsole.scrollHeight;
    }

    // --- PROCESSING SPINNER FEEDBACK ---
    function showProcessing(title = 'Processando documento...', subtitle = 'Convertendo e refinando com IA...') {
        if (spinnerTitle) spinnerTitle.textContent = title;
        if (spinnerSubtitle) spinnerSubtitle.textContent = subtitle;
        if (processingOverlay) processingOverlay.style.display = 'flex';
        if (dropZone) dropZone.classList.add('processing');
    }

    function hideProcessing() {
        if (processingOverlay) processingOverlay.style.display = 'none';
        if (dropZone) dropZone.classList.remove('processing');
    }

    // --- AI TOGGLE INITIALIZATION ---
    if (toggleUseLlm) {
        const savedUseLlm = localStorage.getItem(STORAGE_KEY_USE_LLM);
        if (savedUseLlm !== null) {
            toggleUseLlm.checked = savedUseLlm === 'true';
        }
        toggleUseLlm.addEventListener('change', () => {
            localStorage.setItem(STORAGE_KEY_USE_LLM, toggleUseLlm.checked);
            if (toggleUseLlm.checked) {
                log('✨ Uso de IA ATIVADO (gemma4:26b) para conversão e enriquecimento.', 'info');
            } else {
                log('⚡ Modo NATIVO ativado: conversão rápida sem IA.', 'info');
            }
        });
    }

    // --- METRICS UPDATE ---
    function updateMetrics(text) {
        const chars = text.length;
        const words = text.trim() ? text.trim().split(/\s+/).length : 0;
        const lines = text.split('\n').length;

        metricChars.textContent = chars.toLocaleString();
        metricWords.textContent = words.toLocaleString();
        metricLines.textContent = lines.toLocaleString();

        // Line Numbers counter
        let numsHtml = '';
        for (let i = 1; i <= lines; i++) {
            numsHtml += i + '<br>';
        }
        lineNumbers.innerHTML = numsHtml;
    }

    // --- RENDER CURRENT ACTIVE TAB CONTENT ---
    function renderActiveTab() {
        const fileObj = convertedFiles.find(f => f.id === activeTabId);
        if (!fileObj) return;

        markdownEditor.value = fileObj.markdown || '';
        updateMetrics(fileObj.markdown || '');

        if (typeof marked !== 'undefined') {
            markdownPreview.innerHTML = marked.parse(fileObj.markdown || '');
            // Highlight code blocks
            if (typeof hljs !== 'undefined') {
                markdownPreview.querySelectorAll('pre code').forEach((block) => {
                    hljs.highlightElement(block);
                });
            }
        } else {
            markdownPreview.textContent = fileObj.markdown || '';
        }

        // Atualiza indicador de uso de IA na barra de métricas
        if (metricAiUsage && metricAiModel) {
            if (fileObj.llm_used) {
                metricAiUsage.style.display = 'inline-flex';
                metricAiModel.textContent = `IA: ${fileObj.llm_model || 'Ativa'}`;
                const providerInfo = fileObj.llm_provider ? ` via ${fileObj.llm_provider}` : '';
                const callsInfo = fileObj.llm_calls_count ? ` (${fileObj.llm_calls_count} chamada(s))` : '';
                metricAiUsage.title = `Processado com inteligência artificial (${fileObj.llm_model || 'IA'})${providerInfo}${callsInfo}`;
            } else {
                metricAiUsage.style.display = 'none';
            }
        }

        renderTabs();
        renderFileTree();
    }

    // --- CATEGORY DETECTOR ---
    function getCategoryForExt(ext) {
        ext = ext.toLowerCase();
        if (['.pdf', '.docx', '.pptx', '.xlsx', '.xls', '.doc', '.ppt'].includes(ext)) return 'docs';
        if (['.html', '.htm'].includes(ext)) return 'web';
        if (['.csv', '.json', '.xml'].includes(ext)) return 'data';
        if (['.png', '.jpg', '.jpeg', '.webp', '.bmp', '.mp3', '.wav', '.m4a'].includes(ext)) return 'media';
        if (['.epub', '.zip'].includes(ext)) return 'archive';
        if (['.msg'].includes(ext)) return 'other';
        return 'docs';
    }

    function getIconForExt(ext) {
        ext = (ext || '').toLowerCase();
        if (ext === '.pdf') return 'fa-file-pdf';
        if (['.docx', '.doc'].includes(ext)) return 'fa-file-word';
        if (['.pptx', '.ppt'].includes(ext)) return 'fa-file-powerpoint';
        if (['.xlsx', '.xls', '.csv'].includes(ext)) return 'fa-file-excel';
        if (['.png', '.jpg', '.jpeg', '.webp'].includes(ext)) return 'fa-file-image';
        if (['.mp3', '.wav', '.m4a'].includes(ext)) return 'fa-file-audio';
        if (ext === '.zip') return 'fa-file-zipper';
        if (ext === '.msg') return 'fa-envelope';
        if (ext === '.json' || ext === '.xml') return 'fa-file-code';
        return 'fa-file-lines';
    }

    // --- RENDER SIDEBAR FILE TREE ---
    function renderFileTree() {
        fileTree.innerHTML = '';
        
        let itemsToDisplay = convertedFiles;
        if (currentCategoryFilter !== 'all') {
            itemsToDisplay = convertedFiles.filter(f => f.category === currentCategoryFilter);
        }

        convertedCount.textContent = itemsToDisplay.length;

        if (itemsToDisplay.length === 0) {
            fileTree.innerHTML = `
                <li class="empty-state">
                    <i class="fa-solid fa-folder-open"></i>
                    <p>Nenhum documento nesta categoria</p>
                </li>`;
            return;
        }

        itemsToDisplay.forEach(f => {
            const li = document.createElement('li');
            li.className = `file-item ${f.id === activeTabId ? 'active' : ''}`;
            const iconClass = getIconForExt(f.extension);

            const aiBadgeHtml = f.llm_used ? `
                <span class="badge-ai" title="Documento gerado/enriquecido com IA (${f.llm_model || 'LLM'})">
                    <i class="fa-solid fa-wand-magic-sparkles"></i> IA
                </span>
            ` : '';

            li.innerHTML = `
                <div class="file-info">
                    <i class="fa-solid ${iconClass} file-icon"></i>
                    <span class="file-name" title="${f.title}">${f.title}</span>
                </div>
                ${aiBadgeHtml}
            `;
            li.addEventListener('click', () => {
                activeTabId = f.id;
                renderActiveTab();
            });
            fileTree.appendChild(li);
        });
    }

    // --- RENDER TABS ---
    function renderTabs() {
        tabBar.innerHTML = '';
        convertedFiles.forEach(f => {
            const tab = document.createElement('div');
            tab.className = `tab ${f.id === activeTabId ? 'active' : ''}`;
            const iconClass = getIconForExt(f.extension);
            const aiIconHtml = f.llm_used ? `<i class="fa-solid fa-wand-magic-sparkles tab-ai-icon" title="Enriquecido com IA (${f.llm_model || 'LLM'})"></i>` : '';

            tab.innerHTML = `
                <i class="fa-solid ${iconClass} tab-icon"></i>
                <span class="tab-title">${f.title}</span>
                ${aiIconHtml}
                ${f.id !== 'welcome' ? `<i class="fa-solid fa-xmark close-tab" data-id="${f.id}"></i>` : ''}
            `;

            tab.addEventListener('click', (e) => {
                if (e.target.classList.contains('close-tab')) {
                    e.stopPropagation();
                    closeTab(f.id);
                    return;
                }
                activeTabId = f.id;
                renderActiveTab();
            });

            tabBar.appendChild(tab);
        });
    }

    function closeTab(id) {
        convertedFiles = convertedFiles.filter(f => f.id !== id);
        if (activeTabId === id) {
            activeTabId = convertedFiles.length > 0 ? convertedFiles[convertedFiles.length - 1].id : 'welcome';
        }
        renderActiveTab();
    }

    // --- EDITOR LIVE INPUT LISTENER ---
    markdownEditor.addEventListener('input', () => {
        const fileObj = convertedFiles.find(f => f.id === activeTabId);
        if (fileObj) {
            fileObj.markdown = markdownEditor.value;
            updateMetrics(markdownEditor.value);
            if (typeof marked !== 'undefined') {
                markdownPreview.innerHTML = marked.parse(markdownEditor.value);
                if (typeof hljs !== 'undefined') {
                    markdownPreview.querySelectorAll('pre code').forEach((block) => {
                        hljs.highlightElement(block);
                    });
                }
            }
        }
    });

    // Sync scroll
    markdownEditor.addEventListener('scroll', () => {
        lineNumbers.scrollTop = markdownEditor.scrollTop;
    });

    // --- CATEGORY CHIP FILTERS ---
    document.querySelectorAll('.cat-chip').forEach(chip => {
        chip.addEventListener('click', () => {
            document.querySelectorAll('.cat-chip').forEach(c => c.classList.remove('active'));
            chip.classList.add('active');
            currentCategoryFilter = chip.getAttribute('data-cat');
            renderFileTree();
        });
    });

    // --- UPLOAD HANDLERS ---
    btnTriggerUpload.addEventListener('click', () => fileInput.click());
    dropZone.addEventListener('click', () => fileInput.click());

    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.classList.add('dragover');
    });

    dropZone.addEventListener('dragleave', () => {
        dropZone.classList.remove('dragover');
    });

    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZone.classList.remove('dragover');
        if (e.dataTransfer.files.length > 0) {
            handleFileUpload(e.dataTransfer.files);
        }
    });

    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            handleFileUpload(e.target.files);
        }
    });

    async function handleFileUpload(files) {
        const shouldUseLlm = toggleUseLlm ? toggleUseLlm.checked : true;
        const activeModel = llmModel || 'gemma4:26b';

        showProcessing(
            `Convertendo ${files.length} arquivo(s)...`,
            shouldUseLlm ? `Processando e refinando com IA (${activeModel})...` : 'Processando via conversor nativo ultra-rápido...'
        );

        log(`Iniciando upload e conversão de ${files.length} arquivo(s) (Modo IA: ${shouldUseLlm ? 'Ativado - ' + activeModel : 'Desativado'})...`, 'info');
        
        const formData = new FormData();
        const loadingItems = [];
        for (let i = 0; i < files.length; i++) {
            formData.append('files', files[i]);
            const li = document.createElement('li');
            li.className = 'file-item loading';
            li.innerHTML = `
                <div class="file-info">
                    <i class="fa-solid fa-circle-notch fa-spin file-icon" style="color: var(--accent-cyan);"></i>
                    <span class="file-name">${files[i].name}</span>
                </div>
                <span class="badge-ai"><i class="fa-solid fa-spinner fa-spin"></i> Processando...</span>
            `;
            fileTree.prepend(li);
            loadingItems.push(li);
        }
        formData.append('use_llm', shouldUseLlm);

        try {
            const resp = await fetch('/api/batch-convert', {
                method: 'POST',
                body: formData
            });

            const data = await resp.json();
            if (data.status === 'completed' && data.converted) {
                data.converted.forEach(item => {
                    const ext = item.extension || '.' + item.filename.split('.').pop();
                    const newDoc = {
                        id: 'doc_' + Date.now() + '_' + Math.random().toString(36).substr(2, 4),
                        filename: item.filename,
                        title: item.filename,
                        type: item.type || 'file',
                        category: getCategoryForExt(ext),
                        extension: ext,
                        markdown: item.markdown,
                        llm_used: Boolean(item.llm_used),
                        llm_model: item.llm_model || null,
                        llm_provider: item.llm_provider || null,
                        llm_calls_count: item.llm_calls_count || 0
                    };
                    convertedFiles.push(newDoc);
                    activeTabId = newDoc.id;
                    if (newDoc.llm_used) {
                        log(`[IA] Modelo "${newDoc.llm_model}" gerou/enriqueceu o Markdown de "${item.filename}".`, 'info');
                    }
                    log(`Sucesso: "${item.filename}" convertido para Markdown.`, 'success');
                });

                if (data.errors && data.errors.length > 0) {
                    data.errors.forEach(err => {
                        log(`Erro em "${err.filename}": ${err.error}`, 'error');
                    });
                }

                renderActiveTab();
            }
        } catch (err) {
            log(`Falha ao converter arquivos: ${err.message}`, 'error');
        } finally {
            loadingItems.forEach(el => el.remove());
            hideProcessing();
        }
    }

    // --- URL CONVERTER MODAL ---
    btnOpenUrlModal.addEventListener('click', () => urlModal.classList.add('active'));
    btnCloseUrlModal.addEventListener('click', () => urlModal.classList.remove('active'));
    btnCancelUrl.addEventListener('click', () => urlModal.classList.remove('active'));

    btnSubmitUrl.addEventListener('click', async () => {
        const url = urlInput.value.trim();
        if (!url) return;

        urlModal.classList.remove('active');
        urlInput.value = '';

        const shouldUseLlm = toggleUseLlm ? toggleUseLlm.checked : true;
        const activeModel = llmModel || 'gemma4:26b';

        showProcessing(
            'Convertendo conteúdo da URL...',
            shouldUseLlm ? `Extraindo e refinando com IA (${activeModel})...` : 'Extraindo conteúdo da página...'
        );

        log(`Processando URL: ${url} (Modo IA: ${shouldUseLlm ? 'Ativado - ' + activeModel : 'Desativado'})...`, 'info');

        try {
            const resp = await fetch('/api/convert-url', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ url: url, use_llm: shouldUseLlm })
            });

            const resData = await resp.json();
            if (resData.status === 'success' && resData.data) {
                const item = resData.data;
                const newDoc = {
                    id: 'url_' + Date.now(),
                    filename: item.title || 'URL Document',
                    title: item.title || url,
                    type: item.type || 'web',
                    category: item.type === 'youtube' ? 'web' : (item.type === 'rss' ? 'other' : 'web'),
                    extension: '.html',
                    markdown: item.markdown,
                    llm_used: Boolean(item.llm_used),
                    llm_model: item.llm_model || null,
                    llm_provider: item.llm_provider || null,
                    llm_calls_count: item.llm_calls_count || 0
                };
                convertedFiles.push(newDoc);
                activeTabId = newDoc.id;
                if (newDoc.llm_used) {
                    log(`[IA] Modelo "${newDoc.llm_model}" utilizado na conversão da URL "${item.title}".`, 'info');
                }
                log(`Sucesso: Conteúdo da URL "${item.title}" convertido.`, 'success');
                renderActiveTab();
            }
        } catch (err) {
            log(`Erro ao converter URL: ${err.message}`, 'error');
        } finally {
            hideProcessing();
        }
    });

    // --- SETTINGS MODAL & LLM PROVIDER ---
    // Hints clicáveis de URL
    document.querySelectorAll('.settings-hints .url-hint-tag').forEach(tag => {
        tag.addEventListener('click', () => {
            const targetUrl = tag.getAttribute('data-url');
            if (targetUrl && apiBaseUrlInput) {
                apiBaseUrlInput.value = targetUrl;
                apiBaseUrlInput.focus();
            }
        });
    });

    btnOpenSettings.addEventListener('click', () => {
        if (llmTestFeedback) {
            llmTestFeedback.className = 'llm-test-feedback hidden';
            llmTestFeedback.innerHTML = '';
        }
        settingsModal.classList.add('active');
    });

    btnCloseSettingsModal.addEventListener('click', () => settingsModal.classList.remove('active'));
    btnCancelSettings.addEventListener('click', () => settingsModal.classList.remove('active'));

    // Teste de Conexão com a API e Modelo
    if (btnTestSettings) {
        btnTestSettings.addEventListener('click', async () => {
            const testKey = apiKeyInput.value.trim();
            const testModel = (llmModelInput.value || 'gpt-4o').trim();
            const testBaseUrl = apiBaseUrlInput.value.trim();

            llmTestFeedback.className = 'llm-test-feedback loading';
            llmTestFeedback.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Testando comunicação com o modelo...';
            btnTestSettings.disabled = true;

            try {
                const resp = await fetch('/api/test-llm', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        openai_api_key: testKey,
                        llm_model: testModel,
                        openai_base_url: testBaseUrl
                    })
                });
                const res = await resp.json();
                if (resp.ok && res.status === 'success') {
                    llmTestFeedback.className = 'llm-test-feedback success';
                    llmTestFeedback.innerHTML = `<i class="fa-solid fa-circle-check"></i> ${res.message}`;
                    log(`Teste de IA bem-sucedido: Modelo "${testModel}" pronto em ${res.provider}.`, 'success');
                } else {
                    llmTestFeedback.className = 'llm-test-feedback error';
                    llmTestFeedback.innerHTML = `<i class="fa-solid fa-triangle-exclamation"></i> ${res.message || 'Falha ao testar conexão.'}`;
                    log(`Erro no teste de IA: ${res.message || 'Falha na requisição'}`, 'error');
                }
            } catch (err) {
                llmTestFeedback.className = 'llm-test-feedback error';
                llmTestFeedback.innerHTML = `<i class="fa-solid fa-circle-xmark"></i> Erro de rede: ${err.message}`;
                log(`Falha de rede ao testar IA: ${err.message}`, 'error');
            } finally {
                btnTestSettings.disabled = false;
            }
        });
    }

    // Salvar Configurações
    btnSaveSettings.addEventListener('click', async () => {
        apiKey = apiKeyInput.value.trim();
        llmModel = (llmModelInput.value || 'gpt-4o').trim();
        apiBaseUrl = apiBaseUrlInput.value.trim();

        // Persiste no localStorage do navegador
        try {
            localStorage.setItem(STORAGE_KEY_SETTINGS, JSON.stringify({
                apiKey: apiKey,
                llmModel: llmModel,
                apiBaseUrl: apiBaseUrl
            }));
        } catch (e) {}

        settingsModal.classList.remove('active');
        if (llmTestFeedback) llmTestFeedback.className = 'llm-test-feedback hidden';

        const endpointDisplay = apiBaseUrl || 'OpenAI Oficial';
        log(`Atualizando configurações LLM (Modelo: ${llmModel}, Endpoint: ${endpointDisplay})...`, 'info');

        try {
            const resp = await fetch('/api/settings', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    openai_api_key: apiKey,
                    llm_model: llmModel,
                    openai_base_url: apiBaseUrl
                })
            });
            const res = await resp.json();
            if (res.status === 'success') {
                log(`Configurações salvas. LLM Ativo: ${res.llm_enabled}`, 'success');
                updateStatusPill(res.llm_enabled, llmModel, apiBaseUrl);
            }
        } catch (err) {
            log(`Erro ao salvar configurações: ${err.message}`, 'error');
        }
    });

    function updateStatusPill(enabled, model = llmModel, baseUrl = apiBaseUrl) {
        const dot = llmStatusPill.querySelector('.status-dot');
        const text = llmStatusPill.querySelector('.status-text');
        if (!dot || !text) return;

        if (enabled) {
            dot.className = 'status-dot active';
            let label = `LLM: ${model || 'Ativo'}`;
            if (baseUrl) {
                try {
                    const parsed = new URL(baseUrl);
                    const host = (parsed.hostname === 'localhost' || parsed.hostname === '127.0.0.1') ? 'Local' : parsed.hostname;
                    label += ` (${host})`;
                } catch {
                    label += ' (Custom)';
                }
            } else {
                label += ' (OpenAI)';
            }
            text.textContent = label;
            llmStatusPill.title = `Modelo: ${model} | Endpoint: ${baseUrl || 'https://api.openai.com/v1'}`;
        } else {
            dot.className = 'status-dot disabled';
            text.textContent = 'LLM Desativado (Sem Key/Endpoint)';
            llmStatusPill.title = 'Clique no ícone de engrenagem para configurar API Key e Endpoint';
        }
    }

    async function initSettings() {
        const saved = localStorage.getItem(STORAGE_KEY_SETTINGS);
        if (saved) {
            try {
                const config = JSON.parse(saved);
                apiKey = config.apiKey || '';
                llmModel = config.llmModel || 'gemma4:26b';
                apiBaseUrl = config.apiBaseUrl || 'http://127.0.0.1:11434/v1';

                if (apiKeyInput) apiKeyInput.value = apiKey;
                if (llmModelInput) llmModelInput.value = llmModel;
                if (apiBaseUrlInput) apiBaseUrlInput.value = apiBaseUrl;

                const resp = await fetch('/api/settings', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        openai_api_key: apiKey,
                        llm_model: llmModel,
                        openai_base_url: apiBaseUrl
                    })
                });
                if (resp.ok) {
                    const res = await resp.json();
                    updateStatusPill(res.llm_enabled, llmModel, apiBaseUrl);
                    return;
                }
            } catch (e) {
                console.warn('Erro ao carregar configurações salvas:', e);
            }
        }

        // Fallback: consulta health do backend
        try {
            const resp = await fetch('/api/health');
            if (resp.ok) {
                const data = await resp.json();
                llmModel = data.llm_model || 'gemma4:26b';
                apiBaseUrl = data.openai_base_url || 'http://127.0.0.1:11434/v1';
                if (llmModelInput) llmModelInput.value = llmModel;
                if (apiBaseUrlInput) apiBaseUrlInput.value = apiBaseUrl;
                updateStatusPill(data.llm_enabled, llmModel, apiBaseUrl);
            }
        } catch (e) {}
    }

    // --- VIEW MODE TOGGLES ---
    btnSplitView.addEventListener('click', () => setViewMode('split'));
    btnEditorOnly.addEventListener('click', () => setViewMode('editor'));
    btnPreviewOnly.addEventListener('click', () => setViewMode('preview'));

    function setViewMode(mode) {
        viewMode = mode;
        btnSplitView.classList.remove('active');
        btnEditorOnly.classList.remove('active');
        btnPreviewOnly.classList.remove('active');

        if (mode === 'split') {
            btnSplitView.classList.add('active');
            editorPane.style.display = 'flex';
            previewPane.style.display = 'flex';
        } else if (mode === 'editor') {
            btnEditorOnly.classList.add('active');
            editorPane.style.display = 'flex';
            previewPane.style.display = 'none';
        } else if (mode === 'preview') {
            btnPreviewOnly.classList.add('active');
            editorPane.style.display = 'none';
            previewPane.style.display = 'flex';
        }
    }

    // --- EXPORT & COPY BUTTONS ---
    btnCopyMarkdown.addEventListener('click', () => {
        const text = markdownEditor.value;
        navigator.clipboard.writeText(text).then(() => {
            log('Markdown copiado para a área de transferência!', 'success');
            const orig = btnCopyMarkdown.innerHTML;
            btnCopyMarkdown.innerHTML = '<i class="fa-solid fa-check"></i> Copiado!';
            setTimeout(() => btnCopyMarkdown.innerHTML = orig, 2000);
        });
    });

    btnExportMd.addEventListener('click', () => {
        const fileObj = convertedFiles.find(f => f.id === activeTabId);
        if (!fileObj) {
            log('Nenhum documento ativo para download.', 'warning');
            return;
        }

        const content = markdownEditor.value;
        const blob = new Blob([content], { type: 'text/markdown;charset=utf-8;' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        
        let exportName = fileObj.filename || fileObj.title || 'documento.md';
        if (!exportName.toLowerCase().endsWith('.md')) {
            exportName = exportName.replace(/\.[^/.]+$/, '') + '.md';
        }
        
        a.download = exportName;
        a.click();
        URL.revokeObjectURL(url);
        log(`Download via navegador iniciado para: ${exportName}`, 'success');
    });

    if (btnExportLocalMd) {
        btnExportLocalMd.addEventListener('click', async () => {
            const fileObj = convertedFiles.find(f => f.id === activeTabId);
            if (!fileObj) {
                log('Nenhum documento ativo selecionado para exportar.', 'warning');
                return;
            }

            const content = markdownEditor.value;
            if (!content || !content.trim()) {
                log('O conteúdo Markdown está vazio. Nada para exportar.', 'warning');
                return;
            }

            let exportName = fileObj.filename || fileObj.title || 'documento.md';
            if (!exportName.toLowerCase().endsWith('.md')) {
                exportName = exportName.replace(/\.[^/.]+$/, '') + '.md';
            }

            const origHtml = btnExportLocalMd.innerHTML;
            btnExportLocalMd.disabled = true;
            btnExportLocalMd.innerHTML = '<i class="fa-solid fa-circle-notch fa-spin"></i> Exportando...';

            try {
                const response = await fetch('/api/export', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        filename: exportName,
                        markdown: content
                    })
                });

                if (!response.ok) {
                    const errData = await response.json().catch(() => ({}));
                    throw new Error(errData.detail || 'Falha ao salvar no servidor');
                }

                const result = await response.json();
                const savedPath = result.file_path || `exports/${exportName}`;

                // Abre o terminal se estiver colapsado para visualização imediata do caminho
                if (bottomTerminal && bottomTerminal.classList.contains('collapsed')) {
                    bottomTerminal.classList.remove('collapsed');
                }

                log(`[EXPORTAÇÃO CONCLUÍDA] Arquivo salvo com sucesso em: ${savedPath}`, 'success');
                btnExportLocalMd.innerHTML = '<i class="fa-solid fa-check"></i> Exportado!';
                setTimeout(() => {
                    btnExportLocalMd.innerHTML = origHtml;
                    btnExportLocalMd.disabled = false;
                }, 3500);
            } catch (err) {
                log(`Erro ao exportar arquivo localmente: ${err.message}`, 'error');
                btnExportLocalMd.innerHTML = '<i class="fa-solid fa-triangle-exclamation"></i> Erro';
                setTimeout(() => {
                    btnExportLocalMd.innerHTML = origHtml;
                    btnExportLocalMd.disabled = false;
                }, 3500);
            }
        });
    }

    btnExportHtml.addEventListener('click', () => {
        const fileObj = convertedFiles.find(f => f.id === activeTabId);
        if (!fileObj) return;

        const htmlContent = `<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>${fileObj.title}</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.6; max-width: 900px; margin: 0 auto; padding: 40px 20px; background: #0d1117; color: #c9d1d9; }
        pre { background: #161b22; padding: 16px; border-radius: 8px; overflow-x: auto; }
        table { width: 100%; border-collapse: collapse; }
        th, td { border: 1px solid #30363d; padding: 8px 12px; }
        th { background: #161b22; }
    </style>
</head>
<body>
    ${markdownPreview.innerHTML}
</body>
</html>`;

        const blob = new Blob([htmlContent], { type: 'text/html' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = (fileObj.title || 'document').replace(/[^a-z0-9]/gi, '_').toLowerCase() + '.html';
        a.click();
        URL.revokeObjectURL(url);
        log('Arquivo HTML baixado com sucesso.', 'success');
    });

    // --- TERMINAL TOGGLE ---
    toggleTerminalBtn.addEventListener('click', () => {
        bottomTerminal.classList.toggle('collapsed');
    });
    btnMinimizeTerminal.addEventListener('click', (e) => {
        e.stopPropagation();
        bottomTerminal.classList.toggle('collapsed');
    });
    btnClearLogs.addEventListener('click', (e) => {
        e.stopPropagation();
        terminalConsole.innerHTML = '';
        logsCount = 0;
        logBadge.textContent = '0';
    });

    // --- I18N INITIALIZATION & EVENTS ---
    if (window.i18n) {
        window.i18n.applyTranslations();
    }

    document.querySelectorAll('.lang-switch-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            const chosenLang = btn.getAttribute('data-lang');
            if (window.i18n) {
                window.i18n.setLanguage(chosenLang);
            }
        });
    });

    window.addEventListener('languageChanged', (e) => {
        const newLocale = e.detail.locale;
        const newContent = getWelcomeContent(newLocale);
        const welcomeIndex = convertedFiles.findIndex(f => f.id === 'welcome');
        if (welcomeIndex !== -1) {
            convertedFiles[welcomeIndex].filename = newContent.filename;
            convertedFiles[welcomeIndex].title = newContent.title;
            convertedFiles[welcomeIndex].markdown = newContent.markdown;
        }
        renderFileTree();
        renderTabBar();
        renderActiveTab();
    });

    // --- INITIAL RENDER & SETTINGS INIT ---
    renderActiveTab();
    initSettings();
    if (window.i18n) {
        log(window.i18n.t('terminal_ready'), 'info');
    } else {
        log('MarkItDown Studio IDE initialized. Waiting for files or URLs...', 'info');
    }
});

