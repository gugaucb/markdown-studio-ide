import os
import pytest

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
WORKFLOW_FILE = os.path.join(ROOT_DIR, ".github", "workflows", "desktop-release.yml")


def test_desktop_release_workflow_exists():
    """Valida que o arquivo de workflow de release desktop existe."""
    assert os.path.exists(WORKFLOW_FILE), ".github/workflows/desktop-release.yml não encontrado"


def test_desktop_release_workflow_structure():
    """Valida que o workflow de release desktop possui gatilhos, jobs e passos obrigatórios."""
    with open(WORKFLOW_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # Gatilhos
    assert "push:" in content
    assert "tags:" in content
    assert "workflow_dispatch:" in content

    # Matriz / Runners
    assert "windows-latest" in content
    assert "macos-latest" in content

    # Passos de teste
    assert "pytest" in content

    # Passos de compilação
    assert "build_desktop.py" in content
    assert "installer.iss" in content
    assert "create_dmg.sh" in content

    # Checksums e Release
    assert "SHA256" in content or "sha256" in content
    assert "softprops/action-gh-release" in content
