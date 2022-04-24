#!/bin/bash

echo "Creating Python3 virtual environment"
python3 -m venv venv
source venv/bin/activate
echo "Installing app"
pip install --upgrade pip
pip install --editable .

echo "Creating db tables"
./src/db.py

echo "Load data to database. This may take a few minutes."
./src/load_data.py
echo "Done"
echo 'Activate virtual environment: ". venv/bin/activate" and then enter "bbl_search --help" to see help message'
