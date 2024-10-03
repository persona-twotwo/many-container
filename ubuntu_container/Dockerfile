FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt update && apt install -y \
    openssh-server \
    libnss-ldap \
    libpam-ldap \
    nscd \
    ldap-utils \
    python3 \
    python3-pip \
    supervisor

VOLUME [ "/logs" ]

COPY request_recv /src/request_recv
COPY request_send /src/request_send
COPY requirements.txt /src/requirements.txt

RUN pip3 install -r /src/requirements.txt

RUN mkdir -p /logs

# supervisord 설정 파일 복사
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# SSH 설정
RUN mkdir /var/run/sshd

# NSS 및 LDAP 설정 파일 복사
COPY ldap-setting/nsswitch.conf /etc/nsswitch.conf
COPY ldap-setting/ldap.conf /etc/ldap.conf

# PAM 설정 파일 복사
COPY ldap-setting/common-auth /etc/pam.d/common-auth
COPY ldap-setting/common-account /etc/pam.d/common-account
COPY ldap-setting/common-session /etc/pam.d/common-session
COPY ldap-setting/common-password /etc/pam.d/common-password

# 파일 권한 설정
RUN chmod 644 /etc/pam.d/common-*

# SSH 데몬 설정 파일 복사
COPY ldap-setting/sshd_config /etc/ssh/sshd_config

# nscd 시작 설정
RUN systemctl enable nscd

# supervisord 실행
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
