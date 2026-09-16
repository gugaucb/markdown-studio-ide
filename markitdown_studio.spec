# -*- mode: python ; coding: utf-8 -*-
"""
Especificação PyInstaller para o MarkItDown Studio IDE.
Gera um executável standalone multiplataforma (Windows, macOS, Linux) em modo windowed.
"""

import sys
import os
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

block_cipher = None

# Diretório base do projeto
BASE_DIR = os.path.abspath(SPECPATH)

# Coleta de dados estáticos
datas = [
    (os.path.join(BASE_DIR, "ui"), "ui"),
    (os.path.join(BASE_DIR, "version.py"), "."),
]
datas += collect_data_files("pymupdf")
datas += collect_data_files("pymupdf4llm")
datas += collect_data_files("markitdown")
datas += collect_data_files("magika")
datas += collect_data_files("extract_msg")
datas += collect_data_files("pptx")

# Hidden imports críticos para runtime ASGI, FastAPI, PyWebView e MarkItDown
hiddenimports = [
    # Uvicorn e ASGI
    "uvicorn",
    "uvicorn.logging",
    "uvicorn.loops",
    "uvicorn.loops.auto",
    "uvicorn.loops.asyncio",
    "uvicorn.protocols",
    "uvicorn.protocols.http",
    "uvicorn.protocols.http.auto",
    "uvicorn.protocols.http.h11_impl",
    "uvicorn.protocols.http.httptools_impl",
    "uvicorn.protocols.websockets",
    "uvicorn.protocols.websockets.auto",
    "uvicorn.lifespan",
    "uvicorn.lifespan.on",
    "uvicorn.lifespan.off",
    # FastAPI & Starlette & Pydantic
    "fastapi",
    "starlette",
    "starlette.staticfiles",
    "starlette.responses",
    "starlette.middleware",
    "starlette.middleware.cors",
    "pydantic",
    "pydantic_core",
    "multipart",
    # Motores e Conversores
    "markitdown",
    "pymupdf4llm",
    "pymupdf",
    "fitz",
    "bs4",
    "requests",
    "feedparser",
    "wikipediaapi",
    "extract_msg",
    "youtube_transcript_api",
    # PyWebView e Plataformas Nativas
    "webview",
    "webview.platforms.winforms",
    "webview.platforms.edgechromium",
    "webview.platforms.cocoa",
    "webview.platforms.gtk",
    "webview.platforms.qt",
]

# Exclusões para redução de tamanho de binário e remoção de ferramentas de teste
excludes = [
    "pytest",
    "pytest_mock",
    "_pytest",
    "unittest",
    "IPython",
    "tests",
    "tkinter",
]

# Detecção de ícones disponíveis
icon_path = None
for candidate in [
    os.path.join(BASE_DIR, "packaging", "icons", "app.ico"),
    os.path.join(BASE_DIR, "ui", "favicon.ico"),
]:
    if os.path.exists(candidate):
        icon_path = candidate
        break

a = Analysis(
    [os.path.join(BASE_DIR, "desktop.py")],
    pathex=[BASE_DIR],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=excludes,
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(
    a.pure,
    a.zipped_data,
    cipher=block_cipher,
)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="MarkItDownStudio",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # Windowed mode (sem prompt CMD)
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=icon_path,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name="MarkItDownStudio",
)

# Empacotamento em formato .app para macOS
if sys.platform == "darwin":
    mac_icon = os.path.join(BASE_DIR, "packaging", "icons", "app.icns")
    app = BUNDLE(
        coll,
        name="MarkItDownStudio.app",
        icon=mac_icon if os.path.exists(mac_icon) else None,
        bundle_identifier="com.gugaucb.markitdown-studio-ide",
        info_plist={
            "CFBundleName": "MarkItDown Studio IDE",
            "CFBundleDisplayName": "MarkItDown Studio IDE",
            "CFBundleGetInfoString": "MarkItDown Studio IDE Universal Document Transformer",
            "CFBundleIdentifier": "com.gugaucb.markitdown-studio-ide",
            "CFBundleVersion": "1.1.0",
            "CFBundleShortVersionString": "1.1.0",
            "NSHighResolutionCapable": "True",
        },
    )
