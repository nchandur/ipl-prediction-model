#!/bin/bash

sudo -u postgres psql -d ipl -f process/0_new_tables.sql

sudo -u postgres psql -d ipl -f process/1_batting.sql

sudo -u postgres psql -d ipl -f process/2_bowling.sql

sudo -u postgres psql -d ipl -f process/3_total.sql

sudo -u postgres psql -d ipl -f process/4_extras.sql

sudo -u postgres psql -d ipl -f process/5_details.sql

sudo -u postgres psql -d ipl -f process/6_points.sql

rm -r ./data/preprocessed

python3 -m process.elo