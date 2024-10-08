FROM frolvlad/alpine-glibc:latest

# Python과 Supervisor 설치
RUN apk add --no-cache \
    python3 \
    py3-pip \
    supervisor

VOLUME [ "/logs" ]

COPY request_recv /src/request_recv
# COPY request_send /src/request_send
COPY requirements.txt /src/requirements.txt

RUN pip3 install --no-cache-dir -r /src/requirements.txt --break-system-packages

RUN mkdir -p /logs

# supervisord 설정 파일 복사
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# supervisord 실행
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]