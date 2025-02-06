#!/bin/bash

echo "Creating New Tables"
sudo -u postgres psql -d ipl -f process/0_new_tables.sql > /dev/null 2>&1

echo "Processing Batting"
sudo -u postgres psql -d ipl -f process/1_batting.sql > /dev/null 2>&1

echo "Processing Bowling"
sudo -u postgres psql -d ipl -f process/2_bowling.sql > /dev/null 2>&1

echo "Processing Total"
sudo -u postgres psql -d ipl -f process/3_total.sql > /dev/null 2>&1

echo "Processing Extras"
sudo -u postgres psql -d ipl -f process/4_extras.sql > /dev/null 2>&1

echo "Processing Details"
sudo -u postgres psql -d ipl -f process/5_details.sql > /dev/null 2>&1

echo "Processing Points"
sudo -u postgres psql -d ipl -f process/6_points.sql > /dev/null 2>&1

rm -r ./data/preprocessed

python3 -m process.elo

python3 -m process.win_percentage

python3 -m process.batting_average

python3 -m process.bowling_average

sudo -u postgres psql -d ipl -f process/7_elo.sql > /dev/null 2>&1

python3 -m process.perf_indices