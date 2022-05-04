#!/bin/bash
cd ~/A2
git pull
docker-compose up --build --force-recreate -d api nginx
