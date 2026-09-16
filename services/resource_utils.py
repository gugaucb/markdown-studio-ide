"""
Utilitários de Recursos e Gerenciamento de Rede para o MarkItDown Studio IDE.
Garante compatibilidade entre execução em desenvolvimento e pacotes congelados (PyInstaller).
"""

import os
import sys
import socket
import time
from typing import Optional
import requests


def get_resource_path(relative_path: str = "") -> str:
    """
    Retorna o caminho absoluto para um recurso, funcionando tanto em modo de
    desenvolvimento quanto quando empacotado via PyInstaller (sys._MEIPASS).
    """
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        base_dir = getattr(sys, "_MEIPASS")
    else:
        # services/resource_utils.py -> raiz do projeto é o diretório pai de services/
        current_dir = os.path.dirname(os.path.abspath(__file__))
        base_dir = os.path.dirname(current_dir)

    if not relative_path:
        return os.path.normpath(base_dir)

    return os.path.normpath(os.path.join(base_dir, relative_path))


def is_port_in_use(port: int, host: str = "127.0.0.1") -> bool:
    """
    Verifica se uma porta TCP específica já está em uso na máquina local.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.5)
        try:
            s.bind((host, port))
            return False
        except (socket.error, OSError):
            return True


def find_free_port(start_port: int = 8000, max_attempts: int = 100, host: str = "127.0.0.1") -> int:
    """
    Retorna a porta informada se estiver livre; caso contrário, busca sequencialmente
    a próxima porta livre até o limite de tentativas. Como fallback final, solicita
    uma porta efêmera ao sistema operacional.
    """
    for candidate in range(start_port, start_port + max_attempts):
        if not is_port_in_use(candidate, host):
            return candidate

    # Fallback: solicita uma porta efêmera atribuída pelo SO
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, 0))
        return s.getsockname()[1]


def wait_for_server(health_url: str, timeout: float = 5.0, poll_interval: float = 0.1) -> bool:
    """
    Sonda periodicamente a URL de healthcheck até que responda com sucesso (HTTP 200)
    ou até esgotar o tempo limite estipulado.
    """
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            response = requests.get(health_url, timeout=1.0)
            if response.status_code == 200:
                return True
        except (requests.RequestException, OSError):
            pass
        time.sleep(poll_interval)
    return False
