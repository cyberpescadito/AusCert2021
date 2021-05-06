#!/bin/bash
CDIR=${PWD}
cd ./thp/ex1 && docker-compose stop
cd ${CDIR}/thp/ex2 && docker-compose stop 
sudo rm -rf ./thp/ex1/volumes/elasticsearch/data/*
sudo rm -rf ./thp/ex1/volumes/thehive/data/*
sudo rm -rf ./thp/ex1/volumes/thehive/index/*
sudo rm -rf ./thp/ex1/volumes/thehive/files/*


git pull