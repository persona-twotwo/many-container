import os
import subprocess

def main():
    # subprocess.run(["docker", "rm", "-f", "$(docker", "ps", "-aq", "--filter", "'name=many_ubuntu_*')"])
    os.system("docker rm -f $(docker ps -aq --filter 'name=many_ubuntu_*')")
    return 0

if __name__ == "__main__":
    main()