import os
import subprocess
import time
import aiohttp
import asyncio
import os
import csv
import time
import docker

#progress_counter = 0
#progress_lock = asyncio.Lock()
#failed_counter = 0
#failed_lock = asyncio.Lock()

start_time =0
magnification = 10
# ebpf_path = "/yamong/ebpf-tutorial/src/check_path/check_path"
ebpf_path = "/yamong/youmuu/src/tracepoint_process/process_monitor"
container_csv_path = "/yamong/many-container/container_ips.csv"
repeat_count = 100
total_counter = 0
semaphore_count = 10000



async def check_connection(session, port, file, semaphore):
#    global progress_counter
#    global failed_counter
    async with semaphore:
        url = f"http://localhost:{port}/download/{file}"
        try:
            async with session.get(url, timeout=120) as response:
                response.raise_for_status()
                # print(await response.text())
                # print(f"Successfully connected to {url}")
        except Exception as e:
            print(f"Failed to connect to {url} ({e})")
#            async with failed_lock:
#                failed_counter += 1
#        finally:
#            async with progress_lock:
#                progress_counter += 1
#                if progress_counter % 100 == 0:
#                    print(f"진행도: {(progress_counter/total_counter*100):.2f}%, 실패:{failed_counter}, 시간: {time.time() - start_time}")

async def curl(port_list, file_name):
    semaphore = asyncio.Semaphore(semaphore_count)

    async with aiohttp.ClientSession(
        # connector=aiohttp.TCPConnector(ssl=False, limit=10, force_close=True)
    ) as session:
        tasks = []
        for port in port_list:
            for file in file_name:
                tasks.append(check_connection(session, port, file, semaphore))
        await asyncio.gather(*tasks)

def get_file():
    file_name = ["text_0", "text_1", "text_2", "text_3", "text_4", "text_5", "text_6", "text_7", "text_8", "text_9"]
    with open(container_csv_path, 'r') as f:
        reader = csv.reader(f)
        port_list = []
        for row in reader:
            port_list.append(row[2])
        port_list = port_list[1:]
        file_name *= magnification
        global total_counter
        total_counter = len(port_list) * len(file_name)
        asyncio.run(curl(port_list, file_name))


def up_container():
    files = os.listdir('compose-file')

    files.sort()
    for file in files:
        subprocess.run(['docker', 'compose', '-f', 'compose-file/' + file, 'up', '-d'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

    return 0


def reload_container():
    print("container reload start")
    client = docker.from_env()
    containers = client.containers.list(filters={'name': 'many_ubuntu_*'})
    for container in containers:
        container.remove(force=True)
    os.system("rm -rf /yamong/many-container/logs")
    os.system("mkdir -p /yamong/many-container/logs")
    os.system("rm -rf /yamong/many-container/downloaded")
    os.system("mkdir -p /yamong/many-container/downloaded")
    up_container()
    print("container reload finish. wait 20 sec for container to be ready")
    time.sleep(20)

def copy_log(ebpf_on: bool):
    if ebpf_on:
        os.system(f"cp -r /yamong/many-container/logs/ /logs/{magnification}_{start_time}/logs_ebpf_on")
        os.system(f"cp -r /yamong/many-container/downloaded/ /logs/{magnification}_{start_time}/downloaded_ebpf_on")
    else:
        os.system(f"cp -r /yamong/many-container/logs/ /logs/{magnification}_{start_time}/logs_ebpf_off")
        os.system(f"cp -r /yamong/many-container/downloaded/ /logs/{magnification}_{start_time}/downloaded_ebpf_off")




def run_get_file(count):
    for i in range(count):
        start_time = time.time()
        get_file()
        print(f"Time taken: {time.time() - start_time} seconds")

def run_ebpf_on(): 
    with open("ebpf.log", "w") as log_file:
        ebpf_process = subprocess.Popen([ebpf_path], stdout=log_file, stderr=log_file)

    time.sleep(10)
    return ebpf_process

def run_ebpf_off():
    subprocess.Popen(["pkill", "-f", ebpf_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(10)

def main():
    global start_time
    start_time = int(time.time())
    os.system(f"mkdir -p /logs/{magnification}_{start_time}")
    

    reload_container()

    run_ebpf_on()
    print("eBPF ON")

    run_get_file(repeat_count)


    # os.system(f"cp -r /yamong/many-container/logs/ /logs/{magnification}_{start_time}/logs_ebpf_off")
    # os.system(f"cp -r /yamong/many-container/downloaded/ /logs/{magnification}_{start_time}/downloaded_ebpf_off")
    copy_log(True)

    run_ebpf_off()
    print("wait 10 sec")
    time.sleep(10)
    print("eBPF OFF")
    reload_container()

    run_get_file(repeat_count)

    # os.system(f"cp -r /yamong/many-container/logs /logs/{magnification}_{start_time}/logs_ebpf_on")
    # os.system(f"cp -r /yamong/many-container/downloaded /logs/{magnification}_{start_time}/downloaded_ebpf_on")
    copy_log(False)

    with open(f"/logs/{magnification}_{start_time}/settings.txt", "w") as settings_file:
        settings_file.write("magnification: " + str(magnification) + "\n")
        settings_file.write("ebpf_path: " + ebpf_path + "\n")
        settings_file.write("total_counter: " + str(total_counter) + "\n")
        settings_file.write("repeat_count: " + str(repeat_count) + "\n")

    print("FINISH")

if __name__ == "__main__":
    main()