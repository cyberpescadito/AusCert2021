#!/bin/bash

## init
docker-compose stop
sudo rm -rf ./volumes/elasticsearch/data/*
sudo rm -rf ./volumes/elasticsearch/log/*
sudo rm -rf ./volumes/thehive/data/*
sudo rm -rf ./volumes/thehive/index/*
sudo rm -rf ./volumes/thehive/files/*
sudo chown -R :root volumes
sudo chmod -R g+w volumes 

## Run
docker-compose up -d 