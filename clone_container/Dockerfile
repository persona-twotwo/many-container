FROM alpine:latest

VOLUME [ "/logs" ]

RUN apk update && apk add --no-cache gcc musl-dev

RUN mkdir /src
COPY clone.c /src/clone.c
RUN gcc -O3 -o clone.out /src/clone.c

CMD [ "sh", "-c", "./clone.out > /logs/$CONT_ID.out" ]

