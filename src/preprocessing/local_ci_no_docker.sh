#!/bin/bash
while true
do
    python3 ./1_download_train_schedule.py
    python3 ./2_download_rki_data.py
    sleep 1200
done