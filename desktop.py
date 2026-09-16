"""
MarkItDown Studio IDE - Entrypoint Desktop Dedicado (PyWebView)
Gerencia o ciclo de vida da aplicação desktop nativa e do servidor ASGI.
"""

import sys
import os
import argparse
import threading
import time
import webbrowser
from typing import Optional

# Garante que sys.stdout e sys.stderr nunca sejam None em modo windowed (PyInstaller console=False)
class SafeStream:
    encoding = "utf-8"
    errors = "replace"

    def __init__(self, target_stream=None, log_file=None):
        self.target = target_stream
        self.log_file = log_file

    def isatty(self) -> bool:
        return False

    def readable(self) -> bool:
        return False

    def writable(self) -> bool:
        return True

    def seekable(self) -> bool:
        return False

    def write(self, message):
        if self.target and hasattr(self.target, "write"):
            try:
                self.target.write(message)
            except Exception:
                pass
        if self.log_file:
            try:
                with open(self.log_file, "a", encoding="utf-8") as f:
                    f.write(message)
            except Exception:
                pass

    def flush(self):
        if self.target and hasattr(self.target, "flush"):
            try:
                self.target.flush()
            except Exception:
                pass

_log_file = os.path.join(os.path.expanduser("~"), ".markitdown_studio.log")
if sys.stdout is None:
    sys.stdout = SafeStream(log_file=_log_file)
if sys.stderr is None:
    sys.stderr = SafeStream(log_file=_log_file)

import uvicorn

from app import app
from services.resource_utils import (
    get_resource_path,
    find_free_port,
    is_port_in_use,
    wait_for_server,
)
from version import __version__


class DesktopServerManager:
    """
    Gerencia a inicialização, monitoramento de saúde e encerramento gracioso
    do servidor Uvicorn em uma thread dedicada.
    """

    def __init__(self, host: str = "127.0.0.1", port: int = 8000):
        self.host = host
        self.port = port
        self.config = uvicorn.Config(
            app=app,
            host=self.host,
            port=self.port,
            log_level="warning",
            loop="asyncio",
        )
        self.server = uvicorn.Server(self.config)
        self.thread: Optional[threading.Thread] = None
        self._is_running = False

    @property
    def base_url(self) -> str:
        return f"http://{self.host}:{self.port}"

    @property
    def health_url(self) -> str:
        return f"{self.base_url}/api/health"

    def start(self) -> None:
        """Inicia o servidor Uvicorn em thread secundária daemon."""
        if self._is_running:
            return

        self.thread = threading.Thread(
            target=self.server.run,
            name="UvicornServerThread",
            daemon=True,
        )
        self.thread.start()
        self._is_running = True

    def wait_until_ready(self, timeout: float = 5.0) -> bool:
        """Aguarda confirmação de prontidão do servidor via /api/health."""
        return wait_for_server(self.health_url, timeout=timeout)

    def stop(self, timeout: float = 3.0) -> None:
        """Sinaliza parada graciosa ao Uvicorn e aguarda término da thread."""
        if not self._is_running:
            return

        self.server.should_exit = True
        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=timeout)
        self._is_running = False


def launch_desktop(
    host: str = "127.0.0.1",
    port: int = 8000,
    debug: bool = False,
    force_browser: bool = False,
    headless: bool = False,
) -> int:
    """
    Coordena a inicialização do backend e a exibição da janela nativa do PyWebView.
    """
    # 1. Alocação resiliente de porta
    if port <= 0 or is_port_in_use(port, host):
        selected_port = find_free_port(start_port=port if port > 0 else 8000, host=host)
        print(f"[DESKTOP] Porta {port} ocupada/indisponivel. Utilizando porta livre: {selected_port}")
    else:
        selected_port = port

    # 2. Inicializa o servidor backend
    server_mgr = DesktopServerManager(host=host, port=selected_port)
    print(f"[DESKTOP] Inicializando MarkItDown Studio IDE v{__version__} em {server_mgr.base_url}...")
    server_mgr.start()

    # 3. Aguarda prontidão do endpoint /api/health
    if not server_mgr.wait_until_ready(timeout=6.0):
        print("[ERRO] O servidor backend nao respondeu a tempo ao healthcheck. Abortando.")
        server_mgr.stop()
        return 1

    print("[DESKTOP] Servidor pronto e respondendo com sucesso.")

    # 4. Modo headless (útil para validações de CI/CD ou testes automatizados)
    if headless:
        print("[DESKTOP] Modo headless ativo: encerrando servidor apos verificacao.")
        server_mgr.stop()
        return 0

    # 5. Modo forçado no navegador padrão
    if force_browser:
        print(f"[DESKTOP] Abrindo aplicacao no navegador padrao: {server_mgr.base_url}")
        webbrowser.open(server_mgr.base_url)
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n[DESKTOP] Encerrando servidor por sinal de interrupcao...")
            server_mgr.stop()
            return 0

    # 6. Modo Janela Nativa PyWebView
    try:
        import webview

        window_title = f"MarkItDown Studio IDE v{__version__}"
        print(f"[GUI] Criando janela nativa PyWebView: '{window_title}'...")

        # Tenta localizar o favicon como ícone da janela
        icon_path = get_resource_path(os.path.join("ui", "favicon.ico"))
        if not os.path.exists(icon_path):
            icon_path = None

        window = webview.create_window(
            title=window_title,
            url=server_mgr.base_url,
            width=1400,
            height=900,
            min_size=(900, 600),
            resizable=True,
            confirm_close=False,
            text_select=True,
        )

        def on_closed():
            print("[GUI] Janela PyWebView fechada. Finalizando backend...")
            server_mgr.stop()

        window.events.closed += on_closed

        # Inicia loop visual do PyWebView (bloqueia até a janela ser fechada)
        webview.start(debug=debug)

        # Garantia pós-loop
        server_mgr.stop()
        print("[DESKTOP] Aplicacao finalizada com sucesso.")
        return 0

    except Exception as err:
        print(f"[GUI] Falha ao abrir janela nativa ({err}). Recorrendo ao navegador padrao...")
        webbrowser.open(server_mgr.base_url)
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n[DESKTOP] Encerrando aplicacao...")
            server_mgr.stop()
            return 0


def parse_args():
    parser = argparse.ArgumentParser(
        description="MarkItDown Studio IDE - Launcher Desktop Oficial"
    )
    parser.add_argument(
        "--host",
        type=str,
        default="127.0.0.1",
        help="Host de escuta do servidor ASGI local (padrao: 127.0.0.1)",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Porta de escuta do servidor ASGI local (padrao: 8000)",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Habilita Web Inspector / DevTools na janela do PyWebView",
    )
    parser.add_argument(
        "--browser",
        action="store_true",
        help="Forca abertura no navegador padrao do sistema operacional em vez da janela nativa",
    )
    parser.add_argument(
        "--headless",
        action="store_true",
        help="Inicia o servidor, valida prontidao e encerra sem abrir interface visual (para CI/CD)",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    code = launch_desktop(
        host=args.host,
        port=args.port,
        debug=args.debug,
        force_browser=args.browser,
        headless=args.headless,
    )
    os._exit(code)


if __name__ == "__main__":
    import multiprocessing
    multiprocessing.freeze_support()
    main()
