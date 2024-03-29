#!/bin/bash
CONTAINERS=`docker ps --format "{{.Names}}"`
CDIR=${PWD}
## reset ex1
cd ../ex1/ && docker-compose stop
## reset ex2
cd ${CDIR}
docker-compose stop

## Remove existing containers
for d in ${CONTAINERS}
do
  docker rm $d
done

sudo chown -R :root volumes
sudo chmod -R g+w volumes


sudo rm -rf volumes/mailserver/mysql/*
sudo rm -rf volumes/mailserver/vmail/*
sudo rm -rf volumes/mailserver/log/*
## Run
docker-compose up -d