FROM ubuntu:16.04

WORKDIR /app

RUN apt-get update && apt-get install -y \
 wget \
 ffmpeg \
 sox \
 mp3splt \
 && rm -rf /var/lib/apt/lists/*

COPY noises.sh /app

RUN ./noises.sh

CMD ["/usr/bin/echo", "Ready."]
