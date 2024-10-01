import requests
import csv
import random
import time
import logging

ip = os.environ['HOST_IP']
log_dir = f'/logs/{ip}/'
file = 0

with open('/src/request_send/container_ips.csv', 'r') as f:
    reader = csv.reader(f)
    container_ips = [row[1] for row in reader]

container_ips = container_ips[1:]
while True:
    try:
        time.sleep(1)
        random_ip = random.choice(container_ips)
        file = (file+1)%10
        url = f"http://{random_ip}:8000/download/text_{file}"
        response = requests.get(url)
        if response.status_code == 200:
            print(f"{ip}: Successfully downloaded file from {random_ip}: {url}")
            # save file
            with open(f"/downloaded/{ip}_{file}", "w") as f:
                f.write(response.text)
        else:
            print(f"{ip}: Failed to download file from {random_ip}: {url}")
    except Exception as e:
        print(f"{ip}: Error: {e}")

