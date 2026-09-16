import pytest
import io


@pytest.mark.integration
def test_health_check_endpoint(client):
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "converter_initialized" in data
    assert "llm_model" in data


@pytest.mark.integration
def test_settings_update_endpoint(client):
    payload = {
        "llm_model": "llama3.2:3b",
        "openai_base_url": "http://127.0.0.1:11434/v1"
    }
    response = client.post("/api/settings", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["llm_model"] == "llama3.2:3b"


@pytest.mark.integration
def test_convert_upload_endpoint(client):
    file_content = b"# Document Title\n\nSample content for integration test."
    files = {
        "file": ("test_doc.txt", io.BytesIO(file_content), "text/plain")
    }
    data = {
        "use_llm": "false"
    }
    response = client.post("/api/convert-file", files=files, data=data)
    assert response.status_code == 200
    res_json = response.json()
    assert res_json["status"] == "success"
    result = res_json["data"]
    assert result["filename"] == "test_doc.txt"
    assert result["extension"] == ".txt"
    assert "Document Title" in result["markdown"]


@pytest.mark.integration
def test_export_and_files_list_endpoints(client):
    export_payload = {
        "filename": "integration_test_export.md",
        "markdown": "# Exported Markdown Content\n\nTesting export pipeline."
    }
    export_resp = client.post("/api/export", json=export_payload)
    assert export_resp.status_code == 200
    assert export_resp.json()["status"] == "success"

    # Verify presence in /api/workspace
    files_resp = client.get("/api/workspace")
    assert files_resp.status_code == 200
    files_data = files_resp.json()
    assert "files" in files_data
    exported_names = [f["name"] for f in files_data["files"]]
    assert "integration_test_export.md" in exported_names
