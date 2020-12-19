#!/bin/bash

docker-compose down
sleep 2

docker-compose up -d mosquitto
sleep 1
docker-compose up -d zigbee2mqtt
sleep 5
docker-compose up -d homeassistant
sleep 8
docker-compose up -d appdaemon

