import os
import shutil
import uuid
from typing import List, Dict, Any, Optional

class FileManager:
    def __init__(self, workspace_dir: str):
        self.workspace_dir = os.path.abspath(workspace_dir)
        self.uploads_dir = os.path.join(self.workspace_dir, "uploads")
        self.exports_dir = os.path.join(self.workspace_dir, "exports")
        
        os.makedirs(self.uploads_dir, exist_ok=True)
        os.makedirs(self.exports_dir, exist_ok=True)

    def save_uploaded_file(self, filename: str, content_bytes: bytes) -> str:
        """Saves an incoming uploaded file to the uploads directory."""
        unique_name = f"{uuid.uuid4().hex[:8]}_{filename}"
        file_path = os.path.join(self.uploads_dir, unique_name)
        with open(file_path, "wb") as f:
            f.write(content_bytes)
        return file_path

    def save_export_markdown(self, filename: str, markdown_content: str) -> str:
        """Saves exported markdown to the exports directory."""
        clean_name = filename.replace(" ", "_")
        if not clean_name.endswith(".md"):
            clean_name += ".md"
        
        file_path = os.path.join(self.exports_dir, clean_name)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(markdown_content)
        return file_path

    def list_workspace_files(self) -> List[Dict[str, Any]]:
        """Returns metadata of files present in uploads and exports."""
        file_list = []
        
        # Uploaded files
        if os.path.exists(self.uploads_dir):
            for fname in os.listdir(self.uploads_dir):
                fpath = os.path.join(self.uploads_dir, fname)
                if os.path.isfile(fpath):
                    file_list.append({
                        "name": fname,
                        "path": fpath,
                        "size": os.path.getsize(fpath),
                        "category": "uploads",
                        "extension": os.path.splitext(fname)[1].lower()
                    })

        # Exported Markdown files
        if os.path.exists(self.exports_dir):
            for fname in os.listdir(self.exports_dir):
                fpath = os.path.join(self.exports_dir, fname)
                if os.path.isfile(fpath):
                    file_list.append({
                        "name": fname,
                        "path": fpath,
                        "size": os.path.getsize(fpath),
                        "category": "exports",
                        "extension": os.path.splitext(fname)[1].lower()
                    })

        return file_list

    def clear_uploads(self):
        """Cleans temporary upload files."""
        for fname in os.listdir(self.uploads_dir):
            fpath = os.path.join(self.uploads_dir, fname)
            if os.path.isfile(fpath):
                os.remove(fpath)
            elif os.path.isdir(fpath):
                shutil.rmtree(fpath, ignore_errors=True)
