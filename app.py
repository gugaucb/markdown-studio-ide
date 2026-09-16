import os
import sys
import threading
import time
import webbrowser
from typing import Optional, List
from fastapi import FastAPI, File, UploadFile, Form, HTTPException, Body
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from services.markitdown_service import MarkItDownService
from services.file_manager import FileManager

from version import __version__

# Workspace Path
WORKSPACE_DIR = os.path.dirname(os.path.abspath(__file__))
file_manager = FileManager(WORKSPACE_DIR)
DEFAULT_LLM_MODEL = os.environ.get("DEFAULT_LLM_MODEL", "gemma4:26b")
DEFAULT_BASE_URL = os.environ.get("OPENAI_BASE_URL", "http://127.0.0.1:11434/v1")
markitdown_service = MarkItDownService(
    llm_model=DEFAULT_LLM_MODEL,
    openai_base_url=DEFAULT_BASE_URL
)

app = FastAPI(title="MarkItDown Studio IDE", version=__version__)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Invalidação de Cache para Desenvolvimento
@app.middleware("http")
async def add_no_cache_headers(request, call_next):
    response = await call_next(request)
    if request.url.path == "/" or request.url.path.startswith("/static"):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
    return response

# API Endpoints
@app.get("/api/health")
def health_check():
    has_key = markitdown_service.openai_api_key is not None and len(markitdown_service.openai_api_key) > 0
    has_custom_url = markitdown_service.openai_base_url is not None and len(markitdown_service.openai_base_url) > 0
    llm_enabled = (has_key or has_custom_url) and markitdown_service.md is not None
    return {
        "status": "ok",
        "converter_initialized": markitdown_service.md is not None,
        "llm_enabled": llm_enabled,
        "llm_model": markitdown_service.llm_model,
        "openai_base_url": markitdown_service.openai_base_url
    }

@app.post("/api/settings")
def update_settings(data: dict = Body(...)):
    api_key = data.get("openai_api_key")
    llm_model = data.get("llm_model", "gemma4:26b")
    openai_base_url = data.get("openai_base_url")
    markitdown_service.update_config(
        openai_api_key=api_key,
        llm_model=llm_model,
        openai_base_url=openai_base_url
    )
    has_key = markitdown_service.openai_api_key is not None and len(markitdown_service.openai_api_key) > 0
    has_custom_url = markitdown_service.openai_base_url is not None and len(markitdown_service.openai_base_url) > 0
    llm_enabled = (has_key or has_custom_url) and markitdown_service.md is not None

    return {
        "status": "success",
        "message": "Configurações atualizadas com sucesso!",
        "llm_enabled": llm_enabled,
        "llm_model": markitdown_service.llm_model,
        "openai_base_url": markitdown_service.openai_base_url
    }

@app.post("/api/test-llm")
def test_llm(data: dict = Body(...)):
    api_key = data.get("openai_api_key")
    llm_model = (data.get("llm_model") or "gemma4:26b").strip()
    openai_base_url = data.get("openai_base_url")

    cleaned_base_url = openai_base_url.strip().rstrip("/") if openai_base_url and openai_base_url.strip() else None
    if api_key:
        api_key = api_key.strip()

    # Fallback para endpoint local sem chave
    if cleaned_base_url and not api_key:
        api_key = "ollama"

    if not api_key and not cleaned_base_url:
        return JSONResponse(
            status_code=400,
            content={"status": "error", "message": "Informe uma chave de API ou uma URL de endpoint compatível."}
        )

    # Candidatos a testar com fallback transparente localhost <-> 127.0.0.1
    url_candidates = []
    if cleaned_base_url:
        url_candidates.append(cleaned_base_url)
        if "localhost" in cleaned_base_url:
            url_candidates.append(cleaned_base_url.replace("localhost", "127.0.0.1"))
        elif "127.0.0.1" in cleaned_base_url:
            url_candidates.append(cleaned_base_url.replace("127.0.0.1", "localhost"))
    else:
        url_candidates.append(None)

    last_error = None
    successful_url = None

    from openai import OpenAI
    for cand_url in url_candidates:
        try:
            client_kwargs = {"api_key": api_key, "timeout": 8.0}
            if cand_url:
                client_kwargs["base_url"] = cand_url

            client = OpenAI(**client_kwargs)

            client.chat.completions.create(
                model=llm_model,
                messages=[{"role": "user", "content": "ping"}],
                max_tokens=2
            )
            successful_url = cand_url
            break
        except Exception as e:
            last_error = e

    if successful_url is not None or last_error is None:
        effective_provider = successful_url or "https://api.openai.com/v1"
        return {
            "status": "success",
            "message": f"Conexão com o modelo '{llm_model}' bem-sucedida!",
            "model": llm_model,
            "provider": effective_provider
        }
    else:
        err_str = str(last_error)
        if "Connection error" in err_str or "ConnectError" in err_str or "10061" in err_str:
            friendly_msg = f"Não foi possível conectar ao Ollama/servidor em '{cleaned_base_url}'. Certifique-se de que o Ollama está rodando (ex.: abra o aplicativo Ollama ou execute 'ollama serve')."
        elif "not found" in err_str.lower():
            friendly_msg = f"Modelo '{llm_model}' não encontrado no provedor '{cleaned_base_url}'. Verifique os modelos baixados com 'ollama list'."
        else:
            friendly_msg = f"Erro na conexão com '{llm_model}': {err_str}"

        return JSONResponse(
            status_code=400,
            content={"status": "error", "message": friendly_msg}
        )

@app.post("/api/convert-file")
async def convert_file(file: UploadFile = File(...), use_llm: str = Form("true")):
    try:
        should_use_llm = str(use_llm).strip().lower() in ["true", "1", "yes", "on"]
        content = await file.read()
        file_path = file_manager.save_uploaded_file(file.filename, content)
        result = markitdown_service.convert_file(file_path, filename=file.filename, use_llm=should_use_llm)
        return JSONResponse(content={"status": "success", "data": result})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/batch-convert")
async def batch_convert(files: List[UploadFile] = File(...), use_llm: str = Form("true")):
    should_use_llm = str(use_llm).strip().lower() in ["true", "1", "yes", "on"]
    results = []
    errors = []
    for file in files:
        try:
            content = await file.read()
            file_path = file_manager.save_uploaded_file(file.filename, content)
            res = markitdown_service.convert_file(file_path, filename=file.filename, use_llm=should_use_llm)
            results.append(res)
        except Exception as e:
            errors.append({"filename": file.filename, "error": str(e)})
    
    return JSONResponse(content={
        "status": "completed",
        "converted": results,
        "errors": errors,
        "total": len(files)
    })

@app.post("/api/convert-url")
def convert_url(data: dict = Body(...)):
    url = data.get("url")
    if not url:
        raise HTTPException(status_code=400, detail="URL é obrigatória.")
    raw_use_llm = data.get("use_llm", True)
    should_use_llm = str(raw_use_llm).strip().lower() in ["true", "1", "yes", "on"] if isinstance(raw_use_llm, str) else bool(raw_use_llm)
    try:
        result = markitdown_service.convert_url(url, use_llm=should_use_llm)
        return JSONResponse(content={"status": "success", "data": result})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/export")
def export_markdown(data: dict = Body(...)):
    filename = data.get("filename", "converted_document.md")
    content = data.get("markdown", "")
    try:
        saved_path = os.path.abspath(file_manager.save_export_markdown(filename, content))
        return {
            "status": "success",
            "message": f"Arquivo exportado com sucesso para: {saved_path}",
            "file_path": saved_path,
            "filename": os.path.basename(saved_path),
            "directory": os.path.dirname(saved_path)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/workspace")
def list_workspace():
    return {"files": file_manager.list_workspace_files()}

# Static Files & UI Serving
UI_DIR = os.path.join(WORKSPACE_DIR, "ui")
if os.path.exists(UI_DIR):
    app.mount("/static", StaticFiles(directory=UI_DIR), name="static")

@app.get("/")
def read_root():
    index_file = os.path.join(UI_DIR, "index.html")
    if os.path.exists(index_file):
        return FileResponse(
            index_file,
            headers={
                "Cache-Control": "no-cache, no-store, must-revalidate",
                "Pragma": "no-cache",
                "Expires": "0"
            }
        )
    return HTMLResponse("<h1>MarkItDown Studio IDE Interface visual não encontrada</h1>")


def start_server(host="127.0.0.1", port=8000):
    uvicorn.run(app, host=host, port=port, log_level="error")


if __name__ == "__main__":
    PORT = 8000
    HOST = "127.0.0.1"
    server_thread = threading.Thread(target=start_server, args=(HOST, PORT), daemon=True)
    server_thread.start()

    time.sleep(1.5)
    app_url = f"http://{HOST}:{PORT}"
    print(f"[SERVER] MarkItDown Studio IDE rodando em: {app_url}")

    # Try PyWebView Desktop Window
    try:
        import webview
        print("[GUI] Abrindo janela nativa PyWebView...")
        webview.create_window(
            "MarkItDown Studio IDE",
            app_url,
            width=1400,
            height=900,
            min_size=(900, 600),
            resizable=True
        )
        webview.start()
    except Exception as err:
        print(f"[GUI] PyWebView nao iniciado ({err}). Abrindo no navegador padrao...")
        webbrowser.open(app_url)
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("Encerrando aplicacao.")
