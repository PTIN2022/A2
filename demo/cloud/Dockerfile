# syntax=docker/dockerfile:1
FROM python:3.8-slim-buster
WORKDIR /app
EXPOSE 1883
RUN pip3 install paho-mqtt
COPY . .
CMD ["python3","cloud.py"]
