#!/usr/bin/env bash
# ==============================================================================
# Script de Criação de Imagem de Disco macOS (.dmg) para MarkItDown Studio IDE
# ==============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
DIST_DIR="$ROOT_DIR/dist"
INSTALLERS_DIR="$DIST_DIR/installers"

# Determina versão da aplicação
if [[ -n "${1:-}" ]]; then
    VERSION="$1"
else
    VERSION=$(python3 -c "import sys; sys.path.insert(0, '$ROOT_DIR'); from version import __version__; print(__version__)" 2>/dev/null || echo "1.0.0")
fi

APP_BUNDLE="$DIST_DIR/MarkItDownStudio.app"
DMG_NAME="MarkItDown-Studio-v${VERSION}-macOS.dmg"
DMG_OUT="$INSTALLERS_DIR/$DMG_NAME"

echo "============================================================"
echo "Criando Instalador macOS DMG: $DMG_NAME"
echo "============================================================"

mkdir -p "$INSTALLERS_DIR"

if [[ ! -d "$APP_BUNDLE" ]]; then
    echo "[ERRO] Bundle da aplicacao nao encontrado em: $APP_BUNDLE"
    echo "Execute 'python scripts/build_desktop.py' antes de gerar a imagem de disco."
    exit 1
fi

# Remove DMG anterior se existente
rm -f "$DMG_OUT"

# Estratégia 1: create-dmg (estilizado com drag-and-drop visual)
if command -v create-dmg &>/dev/null; then
    echo "[DMG] Utilizando create-dmg para layout customizado..."
    ICON_ARG=""
    if [[ -f "$ROOT_DIR/packaging/icons/app.icns" ]]; then
        ICON_ARG="--volicon $ROOT_DIR/packaging/icons/app.icns"
    fi

    create-dmg \
        --volname "MarkItDown Studio IDE" \
        $ICON_ARG \
        --window-pos 200 120 \
        --window-size 660 400 \
        --icon-size 128 \
        --icon "MarkItDownStudio.app" 180 170 \
        --hide-extension "MarkItDownStudio.app" \
        --app-drop-link 480 170 \
        --no-internet-enable \
        "$DMG_OUT" \
        "$APP_BUNDLE" || true
else
    # Estratégia 2: hdiutil nativo do macOS (compatível com todos os ambientes Apple)
    echo "[DMG] create-dmg nao encontrado. Utilizando hdiutil nativo..."
    TMP_DIR=$(mktemp -d -t mkdmg-XXXXXX)
    trap 'rm -rf "$TMP_DIR"' EXIT

    # Copia bundle e cria symlink para Applications
    cp -R "$APP_BUNDLE" "$TMP_DIR/"
    ln -s /Applications "$TMP_DIR/Applications"

    hdiutil create \
        -volname "MarkItDown Studio IDE" \
        -srcfolder "$TMP_DIR" \
        -ov \
        -format UDZO \
        "$DMG_OUT"
fi

if [[ -f "$DMG_OUT" ]]; then
    SIZE_MB=$(du -m "$DMG_OUT" | cut -f1)
    echo "[SUCESSO] Imagem DMG gerada com sucesso: $DMG_OUT (${SIZE_MB} MB)"
else
    echo "[ERRO] Falha ao gerar o arquivo DMG."
    exit 1
fi
