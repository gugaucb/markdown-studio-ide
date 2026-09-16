import os
import sys
import pytest
from PIL import Image

from version import __version__

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PACKAGING_DIR = os.path.join(ROOT_DIR, "packaging")


def test_inno_setup_script_structure():
    """Valida que o script do Inno Setup existe e contém diretivas essenciais."""
    iss_file = os.path.join(PACKAGING_DIR, "windows", "installer.iss")
    assert os.path.exists(iss_file), "packaging/windows/installer.iss não encontrado"

    with open(iss_file, "r", encoding="utf-8") as f:
        content = f.read()

    # Diretivas obrigatórias
    assert "AppId=" in content
    assert "AppName=" in content
    assert "MarkItDownStudio.exe" in content
    assert "lzma2" in content
    assert "desktopicon" in content
    assert "app.ico" in content

    # Suporte a idiomas EN e PT-BR
    assert "brazilianportuguese" in content
    assert "english" in content

    # Sincronização de versão padrão
    assert f'#define MyAppVersion "{__version__}"' in content


def test_macos_create_dmg_script():
    """Valida que o script de criação de DMG no macOS está estruturado corretamente."""
    dmg_script = os.path.join(PACKAGING_DIR, "macos", "create_dmg.sh")
    assert os.path.exists(dmg_script), "packaging/macos/create_dmg.sh não encontrado"

    with open(dmg_script, "r", encoding="utf-8") as f:
        content = f.read()

    assert content.startswith("#!/usr/bin/env bash")
    assert "MarkItDownStudio.app" in content
    assert "hdiutil" in content
    assert "create-dmg" in content
    assert "installers" in content


def test_native_app_icons():
    """Valida que os ícones nativos foram gerados e possuem as dimensões esperadas."""
    ico_path = os.path.join(PACKAGING_DIR, "icons", "app.ico")
    png_path = os.path.join(PACKAGING_DIR, "icons", "app.png")
    favicon_path = os.path.join(ROOT_DIR, "ui", "favicon.ico")

    assert os.path.exists(ico_path), "packaging/icons/app.ico não encontrado"
    assert os.path.exists(png_path), "packaging/icons/app.png não encontrado"
    assert os.path.exists(favicon_path), "ui/favicon.ico não encontrado"

    # Valida integridade do ícone PNG
    with Image.open(png_path) as img:
        assert img.size == (512, 512)
        assert img.mode == "RGBA"

    # Valida que o arquivo .ico abre com PIL
    with Image.open(ico_path) as ico:
        assert ico.format == "ICO"
        assert ico.size[0] >= 16


def test_docs_desktop_packaging():
    """Valida que o guia de documentação docs/desktop-packaging.md foi criado."""
    doc_path = os.path.join(ROOT_DIR, "docs", "desktop-packaging.md")
    assert os.path.exists(doc_path), "docs/desktop-packaging.md não encontrado"

    with open(doc_path, "r", encoding="utf-8") as f:
        content = f.read()

    assert "Inno Setup" in content
    assert "create-dmg" in content or "hdiutil" in content
    assert "build_desktop.py" in content
