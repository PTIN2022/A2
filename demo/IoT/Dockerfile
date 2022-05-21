# syntax=docker/dockerfile:1
FROM python:3.8-slim-buster
WORKDIR /app
RUN pip3 install paho-mqtt
COPY . .
CMD ["python3","IoT.py"]
