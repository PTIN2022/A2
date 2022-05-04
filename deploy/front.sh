#!/bin/bash
cd ~/GeSyS-Front
git pull
cd ~/A2
docker-compose up --build --force-recreate -d frontcd ~/GeSyS-Front
git pull
cd ~/A2
docker-compose up --build --force-recreate -d front
