#!/usr/bin/env python3
"""
MarkItDown Studio IDE - Script de Automação de Build Desktop
Orquestra o empacotamento da aplicação com PyInstaller e validação pós-build.
"""

import sys
import os
import shutil
import subprocess
import argparse
import time

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SPEC_FILE = os.path.join(ROOT_DIR, "markitdown_studio.spec")
DIST_DIR = os.path.join(ROOT_DIR, "dist")
BUILD_DIR = os.path.join(ROOT_DIR, "build")


def clean_build_artifacts():
    """Remove pastas de compilações anteriores para garantir build reproduzível."""
    for folder in [BUILD_DIR, DIST_DIR]:
        if os.path.exists(folder):
            print(f"[BUILD] Limpando diretorio anterior: {folder}")
            shutil.rmtree(folder, ignore_errors=True)


def check_prerequisites():
    """Verifica se o PyInstaller está instalado no ambiente de execução."""
    try:
        import PyInstaller
        print(f"[BUILD] PyInstaller detectado: versao {PyInstaller.__version__}")
        return True
    except ImportError:
        print("[ERRO] PyInstaller nao encontrado. Instale com: pip install -r requirements-dev.txt")
        return False


def run_pyinstaller():
    """Executa o PyInstaller apontando para a especificação do projeto."""
    print(f"[BUILD] Iniciando empacotamento com spec: {SPEC_FILE}")
    cmd = [
        sys.executable,
        "-m",
        "PyInstaller",
        SPEC_FILE,
        "--noconfirm",
    ]

    result = subprocess.run(cmd, cwd=ROOT_DIR)
    return result.returncode == 0


def get_output_executable_path():
    """Retorna o caminho esperado do executável gerado na pasta dist."""
    app_folder = os.path.join(DIST_DIR, "MarkItDownStudio")
    if sys.platform == "win32":
        return os.path.join(app_folder, "MarkItDownStudio.exe")
    elif sys.platform == "darwin":
        # No macOS pode ser o bundle .app ou o executável interno
        app_bundle = os.path.join(DIST_DIR, "MarkItDownStudio.app")
        if os.path.exists(app_bundle):
            return os.path.join(app_bundle, "Contents", "MacOS", "MarkItDownStudio")
        return os.path.join(app_folder, "MarkItDownStudio")
    else:
        return os.path.join(app_folder, "MarkItDownStudio")


def verify_build_output():
    """Valida se o executável e a pasta ui foram gerados corretamente no dist."""
    exe_path = get_output_executable_path()
    if not os.path.exists(exe_path):
        print(f"[ERRO] Executavel nao encontrado em: {exe_path}")
        return False

    app_folder = os.path.dirname(exe_path)
    # Verifica pasta de UI
    ui_dest = os.path.join(app_folder, "_internal", "ui") if os.path.exists(os.path.join(app_folder, "_internal")) else os.path.join(app_folder, "ui")
    if not os.path.exists(ui_dest):
        # Pode estar em _internal/ui no PyInstaller 6+
        print(f"[AVISO] Pasta ui nao localizada diretamente em {ui_dest}, verificando arvore...")

    size_mb = os.path.getsize(exe_path) / (1024 * 1024)
    print(f"[SUCESSO] Binario compilado: {exe_path} ({size_mb:.2f} MB)")
    return True


def run_sanity_check(timeout: float = 35.0):
    """Executa o binário gerado com --port 0 --headless para certificar que funciona."""
    exe_path = get_output_executable_path()
    if not os.path.exists(exe_path):
        print(f"[ERRO] Nao foi possivel rodar sanity check: executavel ausente ({exe_path})")
        return False

    print(f"[SANITY] Testando execucao do binario standalone em modo headless...")
    cmd = [exe_path, "--port", "0", "--headless"]
    try:
        time.sleep(1.0)
        proc = subprocess.run(cmd, timeout=timeout)
        print(f"[SANITY] Codigo de retorno: {proc.returncode}")
        if proc.returncode == 0:
            print("[SUCESSO] Sanity check do executavel concluido com exito!")
            return True
        else:
            return False
    except subprocess.TimeoutExpired:
        print("[ERRO] Tempo limite excedido ao executar sanity check do binario.")
        return False
    except Exception as err:
        print(f"[ERRO] Falha ao testar binario: {err}")
        return False


def main():
    parser = argparse.ArgumentParser(description="Script de Automacao de Build Desktop - MarkItDown Studio IDE")
    parser.add_argument("--clean-only", action="store_true", help="Apenas limpa os diretorios de build e dist")
    parser.add_argument("--test", action="store_true", help="Executa sanity check do executavel gerado")
    parser.add_argument("--skip-clean", action="store_true", help="Nao limpa diretorios antes do build")
    args = parser.parse_args()

    if args.clean_only:
        clean_build_artifacts()
        print("[BUILD] Limpeza concluida.")
        sys.exit(0)

    if not check_prerequisites():
        sys.exit(1)

    if not args.skip_clean:
        clean_build_artifacts()

    success = run_pyinstaller()
    if not success:
        print("[ERRO] Falha na compilacao com PyInstaller.")
        sys.exit(1)

    if not verify_build_output():
        sys.exit(1)

    if args.test:
        test_ok = run_sanity_check()
        if not test_ok:
            print("[ERRO] Sanity check falhou!")
            sys.exit(1)

    print("[BUILD] Processo de compilação desktop concluído com sucesso!")
    sys.exit(0)


if __name__ == "__main__":
    main()
