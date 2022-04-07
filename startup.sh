#!/bin/bash

docker-compose up -d mosquitto
sleep 1
docker-compose up -d zigbee2mqtt
sleep 2
docker-compose up -d homeassistant
sleep 20
docker-compose up -d appdaemon

