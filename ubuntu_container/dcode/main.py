from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
import os

app = FastAPI()

@app.get("/{filename}")
async def download_file(filename: str):
    file_path = f"./files/{filename}"  # 파일이 저장된 디렉토리를 적절히 수정하세요
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    try:
        return FileResponse(file_path, filename=filename)
    except PermissionError:
        raise HTTPException(status_code=401, detail="Permission denied to read the file")