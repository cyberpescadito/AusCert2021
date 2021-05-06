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

## Run
docker-compose up -d