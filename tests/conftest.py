import os
import sys
import tempfile
import shutil
import pytest
from fastapi.testclient import TestClient

# Ensure root directory is on sys.path
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from app import app
from services.markitdown_service import MarkItDownService


@pytest.fixture
def client():
    """FastAPI TestClient fixture."""
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def temp_workspace():
    """Provides an isolated directory with mock files for conversion tests."""
    temp_dir = tempfile.mkdtemp(prefix="markitdown_test_")
    
    # Create sample files
    txt_path = os.path.join(temp_dir, "sample.txt")
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write("Hello MarkItDown Studio!\nThis is a sample plain text document.")

    csv_path = os.path.join(temp_dir, "data.csv")
    with open(csv_path, "w", encoding="utf-8") as f:
        f.write("id,name,score\n1,Alice,95\n2,Bob,88\n")

    json_path = os.path.join(temp_dir, "data.json")
    with open(json_path, "w", encoding="utf-8") as f:
        f.write('{"title": "Test JSON", "items": [1, 2, 3]}')

    yield {
        "dir": temp_dir,
        "txt": txt_path,
        "csv": csv_path,
        "json": json_path,
    }

    shutil.rmtree(temp_dir, ignore_errors=True)


@pytest.fixture
def markitdown_service():
    """Provides a clean MarkItDownService instance."""
    return MarkItDownService()
