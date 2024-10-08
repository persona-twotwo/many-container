import psutil
import time

def get_cpu_usage():
    return psutil.cpu_percent(interval=1)

def get_memory_usage():
    memory = psutil.virtual_memory()
    return memory.percent

def print_usage():
    cpu_usage = get_cpu_usage()
    memory_usage = get_memory_usage()
    print(f"CPU Usage: {cpu_usage}%")
    print(f"Memory Usage: {memory_usage}%")
    print("-" * 20)

def monitor_resources(interval=5):
    try:
        while True:
            print_usage()
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\nMonitoring stopped.")

if __name__ == "__main__":
    print("Monitoring CPU and Memory Usage (Press Ctrl+C to stop)")
    monitor_resources()