#!/bin/bash

function errorHandler {
    eval "$@"
    local status=$? 
    if (( status != 0 )); then
        echo "Error occurred. Initialization failed."
        exit 1
    fi
}


echo "Creating Python3 virtual environment"
errorHandler "python3 -m venv venv"
source venv/bin/activate
echo "Installing app"
errorHandler "pip install --upgrade pip"
errorHandler "pip install --editable ."

echo "Creating db tables"
errorHandler "./src/db.py"

echo "Load data to database. This may take a few minutes."
errorHandler "./src/load_data.py"
echo "Done"
echo 'Activate virtual environment: ". venv/bin/activate" and then enter "bbl_search --help" to see help message'
