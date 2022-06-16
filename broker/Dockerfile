# syntax=docker/dockerfile:1
FROM ubuntu:latest
ARG DEBIAN_FRONTEND=noninteractive
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends apt-utils
RUN apt install -y mosquitto && apt install -y mosquitto-clients
COPY . .
CMD ["mosquitto","-c", "mosquitto.conf"]
