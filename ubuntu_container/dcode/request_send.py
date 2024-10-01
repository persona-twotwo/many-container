import requests
import csv
import random
import time
with open('container_ips.csv', 'r') as f:
    reader = csv.reader(f)
    container_ips = [row[1] for row in reader]

container_ips = container_ips[1:]
print(container_ips)

while True:
    try:
        time.sleep(random.uniform(1.01, 10))
        random_ip = random.choice(container_ips)
        random_file = random.randint(0,9)
        url = f"http://{random_ip}:8000/text_{random_file}"
        response = requests.get(url)
        if response.status_code == 200:
            print(f"Successfully downloaded file from {random_ip}: {url}")
        else:
            print(f"Failed to download file from {random_ip}: {url}")
    except Exception as e:
        print(f"Error: {e}")

