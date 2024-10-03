import os
import re

def calculate_average_response_time(log_file: str, path: str = "/download"):
    total_time = 0
    unique_requests = set()

    with open(log_file, 'r') as file:
        for line in file:
            match = re.search(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}) - Client: ([^:]+:\d+) - Server: ([^ ]+) - "(\w+) (/download[^"]*)" (\d+) - (\d+\.\d+)s', line)
            if match:
                timestamp, client, server, method, path, status, time = match.groups()

                # /download로 시작하는 경로만 처리
                if path.startswith('/download'):
                    unique_requests.add((timestamp, client, server, method, path, status, time))

    total_time = sum(float(time) for _, _, _, _, _, _, time in unique_requests)
    request_count = len(unique_requests)

    if request_count > 0:
        avg_time = total_time / request_count
        return avg_time, request_count
    else:
        return 0, 0  # No requests found


def calculate_folder_averages(base_folder: str, log_name: str = 'access.log'):
    folder_averages = {}
    total_time = 0
    total_requests = 0

    # 각 폴더(IP)에서 access.log 처리
    for folder in os.listdir(base_folder):
        folder_path = os.path.join(base_folder, folder)
        log_file_path = os.path.join(folder_path, 'access.log')

        if os.path.isfile(log_file_path):
            avg_time, request_count = calculate_average_response_time(log_file_path)
            folder_averages[folder] = (avg_time, request_count)

            # 전체 합계 계산
            total_time += avg_time * request_count
            total_requests += request_count

    # 전체 평균 계산
    if total_requests > 0:
        overall_avg = total_time / total_requests
    else:
        overall_avg = 0

    return folder_averages, overall_avg, total_requests


# 스크립트 실행
if __name__ == "__main__":
    base_folder = "logs"  # logs 폴더 경로

    folder_averages, overall_avg, total_requests = calculate_folder_averages(base_folder)

    # 각 폴더(IP)별 평균 출력
    for folder, (avg_time, request_count) in folder_averages.items():
        print(f"Folder: {folder}, Average Response Time: {avg_time:.4f}s, Total Requests: {request_count}")

    # 전체 평균 및 총 응답 수 출력
    print(f"\nOverall Average Response Time: {overall_avg:.4f}s")
    print(f"Total number of responses: {total_requests}")
