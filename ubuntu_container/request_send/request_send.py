import requests
import csv
import random
import time
import logging
import os

ip = os.environ['HOST_IP']
log_dir = f'/logs/{ip}/'
file = 0
ip_index = 0
with open('/src/request_send/container_ips.csv', 'r') as f:
    reader = csv.reader(f)
    container_ips = [row[1] for row in reader]

container_ips = container_ips[1:]
count_container_ips = len(container_ips)


while True:
    try:
        time.sleep(0.1)
        ip_index = (ip_index+1)%count_container_ips
        target_ip = container_ips[ip_index]
        file = (file+1)%10
        url = f"http://{target_ip}:8000/download/text_{file}"
        response = requests.get(url)
        if response.status_code == 200:
            print(f"{ip}: Successfully downloaded file from {target_ip}: {url}")
            # save file
            with open(f"/downloaded/{ip}_{target_ip}_{file}", "w") as f:
                f.write(response.text)
        else:
            print(f"{ip}: Failed to download file from {target_ip}: {url}")
    except Exception as e:
        print(f"{ip}: Error: {e}")

