import os
import csv
head_template = """services:
"""

body_template = """
  many_ubuntu_{index}:
    image: ubuntu_container-ldap_ssh_container
    container_name: "many_ubuntu_{index}"
    networks:
      custom_network:
        ipv4_address: {ip}
    volumes:
      - ../logs:/logs
"""

tail_template = """
networks:
  custom_network:
    external: true
"""


def int_to_ip(i):
  return f"10.199.{i//250}.{i%250 + 2}"


UNIT = 15
MAX_CONTAINER = 1000

# rm -rf compose-file
os.system('rm -rf compose-file')

if not os.path.exists('compose-file'):
  os.makedirs('compose-file')

container_ips = []

for i in range(0, MAX_CONTAINER,UNIT):
  content = head_template
  for j in range(0, UNIT):
    if i+j > MAX_CONTAINER:
      break
    index = str(i+j).zfill(5)
    print(index)
    c_ip = int_to_ip(i+j)
    container_ips.append(c_ip)
    content += body_template.format(index=index, ip=c_ip)
  content += tail_template
  with open(f'compose-file/docker-compose-{str(i//UNIT).zfill(5)}.yml', 'w') as f:
    f.write(content)

# container_ips.csv
# container_name,ip
with open('container_ips.csv', 'w') as f:
  writer = csv.writer(f)
  writer.writerow(['container_name', 'ip'])
  for i, ip in enumerate(container_ips):
    writer.writerow([f'many_ubuntu_{str(i).zfill(5)}', ip])
