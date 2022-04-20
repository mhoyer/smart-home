#!/bin/bash

docker-compose --no-ansi up -d mosquitto

sleep 1
docker-compose --no-ansi up -d zigbee2mqtt

sleep 2
docker-compose --no-ansi up -d homeassistant

sleep 60
docker-compose --no-ansi up -d appdaemon

if [[ "$1" == "-d" ]]; then
  echo "Entering the endless sleep loop. Check the logs of all containers for further information"

  while true; do
    sleep 60
  done
fi
