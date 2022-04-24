#!/bin/bash

export $(cat .env | xargs)
echo "Initializing MySQL server"
docker-compose -f mysql.yaml up -d
echo "Waiting for the server to start. It can takes several minutes"
while ! docker-compose -f mysql.yaml \
    exec db mysqladmin ping -h 127.0.0.1 -P 3306 \
    -u ${MYSQL_USER} --password=${MYSQL_PASSWORD} > /dev/null; do
    sleep 1
done
echo "MySQL server is ready"

echo "Creating Python3 virtual environment"
python3 -m venv venv
source venv/bin/activate
echo "Installing dependencies"
pip install --upgrade pip
pip install -r requirements.txt

echo "Creating db tables"
./src/db.py

echo "Load data to database. It can takes several minutes"
./src/load_data.py
echo "Done"
