import requests
import csv
import random
import time
import logging
import aiohttp
import asyncio
import os

FILE_CNT = 10
SERVER_ADDR = "localhost"
DOWNLOAD_DIR = "./downloaded"

log_dir = f'/logs/'

def get_port_list() -> list[str]:
    with open('./container_ips.csv', 'r') as f:
        reader = csv.reader(f)
        container_ips = [row[2] for row in reader]
    return container_ips[1:]  # header 제외 본문만 가져옴

async def req_with_aiohttp(session, port, file_no):
    url = f"http://{SERVER_ADDR}:{port}/download/text_{file_no}"
    filename = f"text_{file_no}_{port}"
    file_path = os.path.join(DOWNLOAD_DIR, filename)

    # 다운로드 디렉토리가 없으면 생성
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    
    try:
        async with session.get(url) as response:
            if response.status == 200:
                content = await response.read()

                # 파일 저장
                with open(file_path, "wb") as f:
                    f.write(content)
                
                # print(f"Successfully downloaded: {filename}")
                return {"success": True, "filename": filename, "size": len(content)}
            else:
                print(f"Failed to download {filename}. Status: {response.status}")
                return {"success": False, "status": response.status, "filename": filename}
    except aiohttp.ClientError as e:
        print(f"Error downloading {filename}: {str(e)}")
        return {"success": False, "error": str(e), "filename": filename}

async def async_all_req_onece():
    port_list = get_port_list()
    file_list = range(FILE_CNT)

    async with aiohttp.ClientSession() as session:
        tasks = [req_with_aiohttp(session, port, file_no) for port in port_list for file_no in file_list]
        results = await asyncio.gather(*tasks)
        
        successful_downloads = sum(1 for r in results if r["success"])
        print(f"\nDownload Summary:")
        print(f"Total attempts: {len(results)}")
        print(f"Successful downloads: {successful_downloads}")
        print(f"Failed downloads: {len(results) - successful_downloads}")
        
        return results

def send_req(port: int, file_no: int):
    url = f"http://{SERVER_ADDR}:{port}/download/text_{file_no}"
    filename = f"text_{file_no}_{port}.txt"
    file_path = os.path.join(DOWNLOAD_DIR, filename)

    try:
        response = requests.get(url)
        if response.status_code == 200:
            # 다운로드 디렉토리가 없으면 생성
            os.makedirs(DOWNLOAD_DIR, exist_ok=True)
            
            # 파일 저장
            with open(file_path, "wb") as f:
                f.write(response.content)
            print(f"Successfully downloaded file from {port}_{file_no}: {url}")
        else:
            print(f"Failed to download file from {port}_{file_no}: {url}")
    except Exception as e:
        print(f"Error downloading {port}_{file_no}: {str(e)}")

def send_all_req_onece():
    port_list = get_port_list()
    
    for port in port_list:
        for file_no in range(FILE_CNT):
            time.sleep(0.1)
            try:
                send_req(port, file_no)
            except Exception as e:
                print(f"{port}_{file_no}: Error: {e}")

def send_req_inf_loop(func):
    while True:
        func()

async def main():
    # 비동기 함수 실행
    start_time = time.time()
    await async_all_req_onece()
    print(time.time() - start_time)
    
    # 동기 함수 실행
    # send_all_req_onece()
    
    # 무한 루프 실행 (비동기)
    # while True:
    #     await async_all_req_onece()
    
    # 무한 루프 실행 (동기)
    # send_req_inf_loop(send_all_req_onece)

if __name__ == "__main__":
    asyncio.run(main())