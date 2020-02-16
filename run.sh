#!/bin/bash

mkdir -p ./mosquitto/data ./mosquitto/log
mkdir -p ./zigbee2mqtt/data

docker-compose up -d
