#!/bin/bash
# Create a systemd service that autostarts & manages a docker-compose instance in the current directory
# by Uli Köhler - https://techoverflow.net
# Licensed as CC0 1.0 Universal
SERVICENAME=docker__$(basename $(pwd))

if [ "$(whoami)" != "root" ]; then
  echo "Sorry, you are not root."
  exit 1
fi


echo "Creating systemd service... /etc/systemd/system/${SERVICENAME}.service"

# Create systemd service file
cat >/etc/systemd/system/$SERVICENAME.service <<EOF
[Unit]
Description=$SERVICENAME
Requires=docker.service
After=docker.service

[Service]
Type=simple
Restart=Always
TimeoutSec=600
User=root
Group=docker
WorkingDirectory=$(pwd)
# Shutdown container (if running) when unit is started
ExecStartPre=$(which docker-compose) --no-ansi -f docker-compose.yaml down
# Start container when unit is started
ExecStart=$(pwd)/startup.sh -d
# Stop container when unit is stopped
ExecStop=$(which docker-compose) --no-ansi -f docker-compose.yaml down

[Install]
WantedBy=multi-user.target
EOF

echo "Enabling systemd service $SERVICENAME"
systemctl enable $SERVICENAME.service

echo "Starting $SERVICENAME"
systemctl start $SERVICENAME.service

