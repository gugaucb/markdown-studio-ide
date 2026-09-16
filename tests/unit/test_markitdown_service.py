import os
import pytest
from unittest.mock import MagicMock
from services.markitdown_service import MarkItDownService, LLMTrackingWrapper


@pytest.mark.unit
def test_service_initialization():
    service = MarkItDownService()
    assert service.llm_model == "gemma4:26b"
    assert service.openai_base_url == "http://127.0.0.1:11434/v1"


@pytest.mark.unit
def test_clean_base_url():
    service = MarkItDownService()
    assert service._clean_base_url("http://127.0.0.1:11434") == "http://127.0.0.1:11434"
    assert service._clean_base_url("http://127.0.0.1:11434/v1/") == "http://127.0.0.1:11434/v1"
    assert service._clean_base_url("") is None


@pytest.mark.unit
def test_convert_txt_file(markitdown_service, temp_workspace):
    res = markitdown_service.convert_file(temp_workspace["txt"], use_llm=False)
    assert res is not None
    assert res["filename"] == "sample.txt"
    assert res["extension"] == ".txt"
    assert "Hello MarkItDown Studio!" in res["markdown"]


@pytest.mark.unit
def test_convert_csv_file(markitdown_service, temp_workspace):
    res = markitdown_service.convert_file(temp_workspace["csv"], use_llm=False)
    assert res is not None
    assert res["type"] == "data"
    assert "| id | name | score |" in res["markdown"]
    assert "| Alice |" in res["markdown"]


@pytest.mark.unit
def test_convert_json_file(markitdown_service, temp_workspace):
    res = markitdown_service.convert_file(temp_workspace["json"], use_llm=False)
    assert res is not None
    assert "Test JSON" in res["markdown"]


@pytest.mark.unit
def test_convert_nonexistent_file(markitdown_service):
    with pytest.raises(FileNotFoundError):
        markitdown_service.convert_file("nonexistent_path_test_123.pdf")


@pytest.mark.unit
def test_llm_tracking_wrapper():
    mock_client = MagicMock()
    mock_choice = MagicMock()
    mock_choice.message.content = "Refined content"
    mock_client.chat.completions.create.return_value.choices = [mock_choice]

    tracker = LLMTrackingWrapper(mock_client)
    assert not tracker.was_called
    assert tracker.call_count == 0

    # Simulate completion call
    response = tracker.chat.completions.create(model="test-model", messages=[])
    assert tracker.was_called
    assert tracker.call_count == 1
    assert tracker.last_model_used == "test-model"

    tracker.reset()
    assert tracker.call_count == 0
    assert not tracker.was_called


@pytest.mark.unit
def test_refine_markdown_with_llm_encoding_correction():
    service = MarkItDownService()
    
    mock_client = MagicMock()
    mock_choice = MagicMock()
    # Simulates the LLM repairing the corrupted character 'Ã§Ã£o' to 'ação'
    mock_choice.message.content = "## Configuração do Sistema\n\nTexto com acentuação correta e tabela preservada:\n\n| Item | Valor |\n|---|---|\n| Ação | OK |"
    mock_client.chat.completions.create.return_value.choices = [mock_choice]
    service.llm_client = mock_client

    corrupted_sample = "## ConfiguraÃ§Ã£o do Sistema\n\nTexto com acentuaÃ§Ã£o correta e tabela preservada:\n\n| Item | Valor |\n|---|---|\n| Ação | OK |"
    refined = service.refine_markdown_with_llm(corrupted_sample, "teste.md", ".md")
    
    assert "Configuração do Sistema" in refined
    assert "| Item | Valor |" in refined
    assert "|---|---|" in refined


@pytest.mark.unit
def test_refine_markdown_preserves_table_on_removal_safeguard():
    service = MarkItDownService()
    
    mock_client = MagicMock()
    mock_choice = MagicMock()
    # Simulates an errant LLM response that stripped the table
    mock_choice.message.content = "Summary without table"
    mock_client.chat.completions.create.return_value.choices = [mock_choice]
    service.llm_client = mock_client

    original = "Document with table:\n| Col1 | Col2 |\n|---|---|\n| A | B |"
    # Safeguard should detect table removal and return original intact
    result = service.refine_markdown_with_llm(original, "test.md", ".md")
    assert "| Col1 | Col2 |" in result
    assert "|---|---|" in result
