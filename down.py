import os
import subprocess

os.system('docker rm -f $(docker ps -aq --filter "name=many_ubuntu_*")')