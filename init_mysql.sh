#!/bin/bash

export $(cat .env | xargs)
echo "Initializing MySQL server"
docker-compose -f mysql.yaml up -d
echo "Waiting for the server to start. This may take a few minutes"
while ! docker-compose -f mysql.yaml \
    exec db mysqladmin ping -h 127.0.0.1 -P 3306 \
    -u ${MYSQL_USER} --password=${MYSQL_PASSWORD} > /dev/null; do
    sleep 1
done
echo "MySQL server is ready"
