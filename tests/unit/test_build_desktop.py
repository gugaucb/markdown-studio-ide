import os
import sys
import shutil
import pytest
from unittest.mock import patch

from scripts.build_desktop import (
    SPEC_FILE,
    clean_build_artifacts,
    check_prerequisites,
    get_output_executable_path,
)


def test_spec_file_structure():
    """Valida que o arquivo markitdown_studio.spec existe e contém configurações obrigatórias."""
    assert os.path.exists(SPEC_FILE), "markitdown_studio.spec não foi encontrado"

    with open(SPEC_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # Verifica entrypoint
    assert "desktop.py" in content

    # Verifica inclusão de datas obrigatórias
    assert '"ui"' in content or "'ui'" in content
    assert '"version.py"' in content or "'version.py'" in content

    # Verifica imports críticos
    assert "uvicorn" in content
    assert "fastapi" in content
    assert "markitdown" in content
    assert "webview" in content

    # Verifica modo windowed (sem prompt DOS)
    assert "console=False" in content

    # Verifica nome do executável
    assert 'name="MarkItDownStudio"' in content or "name='MarkItDownStudio'" in content


def test_check_prerequisites():
    """Valida a detecção de presença do PyInstaller."""
    assert check_prerequisites() is True


def test_clean_build_artifacts(tmp_path, monkeypatch):
    """Valida limpeza dos diretórios de build temporários."""
    mock_build = tmp_path / "build"
    mock_dist = tmp_path / "dist"
    mock_build.mkdir()
    mock_dist.mkdir()

    (mock_build / "temp.txt").write_text("build artifact")
    (mock_dist / "output.exe").write_text("bin artifact")

    monkeypatch.setattr("scripts.build_desktop.BUILD_DIR", str(mock_build))
    monkeypatch.setattr("scripts.build_desktop.DIST_DIR", str(mock_dist))

    clean_build_artifacts()

    assert not mock_build.exists()
    assert not mock_dist.exists()


def test_get_output_executable_path():
    """Valida a resolução do caminho do executável gerado."""
    path = get_output_executable_path()
    assert "MarkItDownStudio" in path
    if sys.platform == "win32":
        assert path.endswith(".exe")
