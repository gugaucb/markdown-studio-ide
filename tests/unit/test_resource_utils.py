import os
import sys
import socket
from unittest.mock import patch, MagicMock
import requests

from services.resource_utils import (
    get_resource_path,
    is_port_in_use,
    find_free_port,
    wait_for_server,
)


def test_get_resource_path_dev_mode():
    """Valida que em modo desenvolvimento os caminhos são relativos à raiz do projeto."""
    root_path = get_resource_path()
    assert os.path.exists(root_path)
    assert os.path.exists(os.path.join(root_path, "services"))

    ui_path = get_resource_path("ui")
    assert os.path.exists(ui_path)
    assert os.path.isdir(ui_path)


def test_get_resource_path_frozen_mode(monkeypatch):
    """Valida que em modo empacotado (PyInstaller) sys._MEIPASS é respeitado."""
    fake_meipass = r"C:\Temp\_MEI12345" if sys.platform == "win32" else "/tmp/_MEI12345"
    monkeypatch.setattr(sys, "frozen", True, raising=False)
    monkeypatch.setattr(sys, "_MEIPASS", fake_meipass, raising=False)

    resolved = get_resource_path(os.path.join("ui", "index.html"))
    expected = os.path.normpath(os.path.join(fake_meipass, "ui", "index.html"))
    assert resolved == expected


def test_is_port_in_use_and_find_free_port():
    """Testa detecção de porta ocupada e alocação dinâmica de porta livre."""
    # Encontra uma porta livre
    free_port = find_free_port(start_port=9100)
    assert not is_port_in_use(free_port)

    # Ocupa a porta temporariamente com um socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", free_port))
        s.listen(1)
        assert is_port_in_use(free_port)

        # find_free_port a partir dessa porta deve encontrar outra
        next_port = find_free_port(start_port=free_port)
        assert next_port != free_port
        assert not is_port_in_use(next_port)


def test_wait_for_server_timeout():
    """Valida retorno False quando a URL de healthcheck não responde dentro do tempo."""
    free_port = find_free_port(start_port=9200)
    result = wait_for_server(f"http://127.0.0.1:{free_port}/api/health", timeout=0.2, poll_interval=0.05)
    assert result is False


def test_wait_for_server_success(monkeypatch):
    """Valida retorno True quando a URL responde com status 200."""
    mock_resp = MagicMock()
    mock_resp.status_code = 200

    with patch("requests.get", return_value=mock_resp):
        result = wait_for_server("http://127.0.0.1:8000/api/health", timeout=1.0)
        assert result is True
