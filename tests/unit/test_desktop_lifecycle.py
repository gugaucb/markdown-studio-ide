import time
import pytest
from desktop import DesktopServerManager, launch_desktop, parse_args
from services.resource_utils import find_free_port, is_port_in_use


def test_desktop_server_manager_lifecycle():
    """Testa inicialização em background, verificação de health e parada graciosa."""
    port = find_free_port(start_port=8850)
    server_mgr = DesktopServerManager(host="127.0.0.1", port=port)

    assert server_mgr.base_url == f"http://127.0.0.1:{port}"
    assert server_mgr.health_url == f"http://127.0.0.1:{port}/api/health"

    # Inicia o servidor
    server_mgr.start()

    try:
        # Aguarda prontidão
        ready = server_mgr.wait_until_ready(timeout=5.0)
        assert ready is True

        # Verifica que a porta agora está em uso
        assert is_port_in_use(port)
    finally:
        # Para graciosamente
        server_mgr.stop(timeout=3.0)

    # Dá um breve intervalo para o socket ser liberado pelo SO
    time.sleep(0.5)
    assert not is_port_in_use(port)


def test_launch_desktop_headless():
    """Valida execução completa da função launch_desktop no modo headless."""
    port = find_free_port(start_port=8900)
    code = launch_desktop(
        host="127.0.0.1",
        port=port,
        debug=False,
        force_browser=False,
        headless=True,
    )
    assert code == 0


def test_parse_args(monkeypatch):
    """Testa o parser de argumentos de linha de comando."""
    test_args = ["desktop.py", "--host", "0.0.0.0", "--port", "9090", "--debug", "--browser"]
    monkeypatch.setattr("sys.argv", test_args)

    args = parse_args()
    assert args.host == "0.0.0.0"
    assert args.port == 9090
    assert args.debug is True
    assert args.browser is True
    assert args.headless is False
