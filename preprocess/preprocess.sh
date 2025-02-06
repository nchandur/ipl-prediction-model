#!/bin/bash

echo "Creating Database"
sudo -u postgres psql -d postgres -f preprocess/load.sql > /dev/null 2>&1

echo "Processing batting and bowling stats..."
python3 preprocess/bat_bowl.py

echo "Processing match details..."
python3 preprocess/details.py

python3 preprocess/csvToDB.py

echo "Preprocessing Complete!"