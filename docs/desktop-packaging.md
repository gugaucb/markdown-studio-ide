# 📦 Guia de Empacotamento Desktop (Windows & macOS)

Este documento descreve a arquitetura, pré-requisitos e procedimentos passo a passo para compilar e gerar instaladores nativos do **MarkItDown Studio IDE** para distribuição desktop em **Windows (.exe)** e **macOS (.dmg)**.

---

## 🏛️ Arquitetura Desktop

O **MarkItDown Studio IDE Desktop** adota uma arquitetura leve e nativa:
- **Motor Web Nativo**: Utiliza o [PyWebView](https://pywebview.flowrl.com/) conectado ao Microsoft Edge WebView2 (no Windows) e ao WebKit/WKWebView (no macOS). Ao contrário de soluções baseadas em Electron que embutem um navegador Chromium completo (~150MB+), a aplicação utiliza o runtime nativo do sistema operacional, resultando em menor consumo de memória e pacotes menores.
- **Runtime Local**: O backend FastAPI/Uvicorn executa em thread secundária daemon vinculada a uma porta local alocada dinamicamente, garantindo suporte aos mesmos endpoints e pipelines de conversão de documentos.
- **Congelamento**: O [PyInstaller](https://pyinstaller.org/) empacota o interpretador Python, dependências e modelos em modo windowed (`--noconsole`).
- **Instaladores**: 
  - Windows: [Inno Setup](https://jrsoftware.org/isinfo.php) para gerar setup único com atalhos e desinstalador.
  - macOS: [create-dmg](https://github.com/create-dmg/create-dmg) / `hdiutil` para gerar imagem de disco com instalação drag-and-drop.

---

## 📋 Pré-requisitos

### Pré-requisitos Comuns (Todas as Plataformas)
1. Python 3.10 ou superior (recomendado 3.11+).
2. Dependências de desenvolvimento instaladas:
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```

### Específicos para Windows
- **Microsoft Edge WebView2 Runtime**: Pré-instalado por padrão no Windows 10 e Windows 11.
- **Inno Setup 6**: Necessário para compilar o instalador `.exe`. Pode ser instalado via Chocolatey ou instalador oficial:
  ```powershell
  choco install innosetup
  # ou winget
  winget install JRSoftware.InnoSetup
  ```

### Específicos para macOS
- **Xcode Command Line Tools**:
  ```bash
  xcode-select --install
  ```
- **create-dmg** (opcional, para visual estilizado):
  ```bash
  brew install create-dmg
  ```

---

## 🛠️ Passo 1: Compilar o Executável Standalone

O script de automação [scripts/build_desktop.py](../scripts/build_desktop.py) orquestra a limpeza, validação de assets e compilação via PyInstaller:

```bash
# Compilar e executar sanity check automatizado
python scripts/build_desktop.py --test
```

### O que o script faz:
1. Limpa pastas `build/` e `dist/` anteriores.
2. Executa o PyInstaller com a especificação [markitdown_studio.spec](../markitdown_studio.spec).
3. Coleta os arquivos estáticos da pasta `ui/` e modelos de IA (`magika`, `pymupdf`, etc.).
4. Testa a execução do binário gerado na pasta `dist/MarkItDownStudio/` em modo headless.

---

## 🪟 Passo 2 (Windows): Gerar Instalador (.exe) via Inno Setup

Com a pasta `dist/MarkItDownStudio/` gerada, execute o compilador do Inno Setup:

```powershell
# Executa compilação do instalador passando a versão
& "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" /DMyAppVersion=1.0.0 packaging\windows\installer.iss
```

O instalador será gerado em:
```text
dist/installers/MarkItDown-Studio-Setup-v1.0.0-Windows-x64.exe
```

### Características do Instalador Windows:
- Compressão máxima `lzma2/ultra64`.
- Suporte a idiomas Português do Brasil e Inglês.
- Criação de atalhos opcionais na Área de Trabalho e no Menu Iniciar.
- Ícone nativo multi-resolução integrado (`packaging/icons/app.ico`).
- Desinstalador limpo e registrado no Painel de Controle.

---

## 🍎 Passo 2 (macOS): Gerar Imagem de Disco (.dmg)

No macOS, após a compilação do bundle `dist/MarkItDownStudio.app`:

```bash
# Permissão de execução no script
chmod +x packaging/macos/create_dmg.sh

# Gera a imagem .dmg
./packaging/macos/create_dmg.sh
```

A imagem de disco será salva em:
```text
dist/installers/MarkItDown-Studio-v1.0.0-macOS.dmg
```

O usuário pode instalar o aplicativo arrastando o ícone para a pasta `/Applications`.

---

## 🎨 Gerar ou Atualizar Ícones Nativos

Para regenerar os ícones nativos a partir do template visual em alta resolução:

```bash
python packaging/icons/generate_icons.py
```

Arquivos gerados:
- `packaging/icons/app.ico`: Ícone do Windows com camadas 16x16, 24x24, 32x32, 48x48, 64x64, 128x128 e 256x256.
- `packaging/icons/app.png`: Versão de 512x512 pixels para documentação.
- `ui/favicon.ico`: Favicon sincronizado da interface web.

---

## ❓ Solução de Problemas (Troubleshooting)

### Janela em branco no Windows
- Certifique-se de que o Microsoft Edge WebView2 está instalado e atualizado.
- Execute com `--debug` ou verifique o arquivo de log gerado em `%USERPROFILE%\.markitdown_studio.log`.

### Porta já em uso
- O `desktop.py` detecta automaticamente se a porta `8000` está ocupada e seleciona a próxima porta livre (ex: `8001`, `8002`), sem interromper a inicialização da aplicação.
