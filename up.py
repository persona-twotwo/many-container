import os
import subprocess

# ls compose-file
# docker compose -f compose-file/docker-compose-0.yml up -d

files = os.listdir('compose-file')

files.sort()
count = 0
for file in files:
    count += 1
    print(count)
    subprocess.run(['docker', 'compose', '-f', 'compose-file/' + file, 'up', '-d'])