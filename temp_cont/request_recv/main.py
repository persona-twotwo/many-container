import os
import logging
from pathlib import Path
from datetime import datetime
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse
from starlette.middleware.base import BaseHTTPMiddleware

def setup_logging():
    try:
        CONT_ID = os.environ.get('CONT_ID')
        if not CONT_ID:
            raise ValueError("CONT_ID environment variable is not set")

        log_dir = (f'/logs/{CONT_ID}_')

        # 파일 접근 로그 설정
        file_logger = logging.getLogger('file_access')
        file_logger.setLevel(logging.INFO)
        if not file_logger.handlers:
            file_handler = logging.FileHandler(log_dir + 'file_access.log')
            file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
            file_logger.addHandler(file_handler)

        # 전체 접근 로그 설정
        access_logger = logging.getLogger('access')
        access_logger.setLevel(logging.INFO)
        if not access_logger.handlers:
            access_handler = logging.FileHandler(log_dir + 'access.log')
            access_handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
            access_logger.addHandler(access_handler)

        print(f"Logging setup completed. Log directory: {log_dir}")
        return file_logger, access_logger
    except Exception as e:
        print(f"Error setting up logging: {e}")
        raise

# 로깅 설정 실행
file_logger, access_logger = setup_logging()

app = FastAPI()

class AccessLogMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = datetime.now()
        response = await call_next(request)
        process_time = (datetime.now() - start_time).total_seconds()
        
        client_host, client_port = request.client.host, request.client.port
        server_host, server_port = request.url.hostname, request.url.port
        
        log_msg = (f"Client: {client_host}:{client_port} - "
                   f"Server: {server_host}:{server_port} - "
                   f"\"{request.method} {request.url.path}\" "
                   f"{response.status_code} - {process_time}s")
        access_logger.info(log_msg)
        
        return response

app.add_middleware(AccessLogMiddleware)

@app.get("/download/{filename}")
async def download_file(filename: str):
    file_path = Path(f"/src/request_recv/files/{filename}")
    
    if not file_path.exists():
        file_logger.warning(f"File not found: {filename}")
        raise HTTPException(status_code=404, detail="File not found")
    
    try:
        file_logger.info(f"File download attempt: {filename}")
        return FileResponse(str(file_path), filename=filename)
    except PermissionError:
        file_logger.error(f"Permission denied to read file: {filename}")
        raise HTTPException(status_code=401, detail="Permission denied to read the file")
    except Exception as e:
        file_logger.error(f"Error occurred while trying to download file {filename}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)