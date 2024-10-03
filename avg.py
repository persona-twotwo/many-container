import os
import re

def calculate_response_times(log_file: str, path: str = "/download"):
    total_time = 0
    unique_requests = set()
    slowest_time = 0
    slowest_request = None

    with open(log_file, 'r') as file:
        for line in file:
            match = re.search(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}) - Client: ([^:]+:\d+) - Server: ([^ ]+) - "(\w+) (/download[^"]*)" (\d+) - (\d+\.\d+)s', line)
            if match:
                timestamp, client, server, method, path, status, time = match.groups()

                # /download로 시작하는 경로만 처리
                if path.startswith('/download'):
                    time_float = float(time)
                    unique_requests.add((timestamp, client, server, method, path, status, time_float))
                    
                    if time_float > slowest_time:
                        slowest_time = time_float
                        slowest_request = (timestamp, path, time_float)

    total_time = sum(time for _, _, _, _, _, _, time in unique_requests)
    request_count = len(unique_requests)

    if request_count > 0:
        avg_time = total_time / request_count
        return avg_time, request_count, slowest_time, slowest_request
    else:
        return 0, 0, 0, None  # No requests found

def calculate_folder_averages(base_folder: str, log_name: str = 'access.log'):
    folder_stats = {}
    total_time = 0
    total_requests = 0
    overall_slowest_time = 0
    overall_slowest_request = None

    # 각 폴더(IP)에서 access.log 처리
    for folder in os.listdir(base_folder):
        folder_path = os.path.join(base_folder, folder)
        log_file_path = os.path.join(folder_path, log_name)

        if os.path.isfile(log_file_path):
            avg_time, request_count, slowest_time, slowest_request = calculate_response_times(log_file_path)
            folder_stats[folder] = {
                'avg_time': avg_time,
                'request_count': request_count,
                'slowest_time': slowest_time,
                'slowest_request': slowest_request
            }

            # 전체 합계 계산
            total_time += avg_time * request_count
            total_requests += request_count

            # 전체 가장 느린 응답 업데이트
            if slowest_time > overall_slowest_time:
                overall_slowest_time = slowest_time
                overall_slowest_request = (folder,) + slowest_request

    # 전체 평균 계산
    overall_avg = total_time / total_requests if total_requests > 0 else 0

    return folder_stats, overall_avg, total_requests, overall_slowest_time, overall_slowest_request

# 스크립트 실행
if __name__ == "__main__":
    base_folder = "logs"  # logs 폴더 경로

    folder_stats, overall_avg, total_requests, overall_slowest_time, overall_slowest_request = calculate_folder_averages(base_folder)

    # 각 폴더(IP)별 통계 출력
    for folder, stats in folder_stats.items():
        print(f"\nFolder: {folder}")
        print(f"  Average Response Time: {stats['avg_time']:.5f}s")
        print(f"  Total Requests: {stats['request_count']}")
        print(f"  Slowest Response Time: {stats['slowest_time']:.5f}s")
        if stats['slowest_request']:
            print(f"  Slowest Request: {stats['slowest_request'][0]} - {stats['slowest_request'][1]}")

    # 전체 통계 출력
    print(f"\nOverall Statistics:")
    print(f"Overall Average Response Time: {overall_avg:.5f}s")
    print(f"Total number of responses: {total_requests}")
    print(f"Overall Slowest Response Time: {overall_slowest_time:.5f}s")
    if overall_slowest_request:
        print(f"Overall Slowest Request: {overall_slowest_request[0]} - {overall_slowest_request[1]} - {overall_slowest_request[2]}")