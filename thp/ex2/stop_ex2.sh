#!/bin/bash
CONTAINERS=`docker ps --format "{{.Names}}"`
CDIR=${PWD}

## Run
docker-compose stop
## Remove existing containers
for d in ${CONTAINERS}
do
  docker rm $d
done

sudo rm -rf volumes/mailserver/mysql/*
sudo rm -rf volumes/mailserver/vmail/*
sudo rm -rf volumes/mailserver/log/*
