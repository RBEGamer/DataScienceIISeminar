#!/bin/bash
while true
do
    git pull
    python3 ./1_download_train_schedule.py
#    python3 ./2_download_rki_data.py
    git pull
    git add .
    git commit -m "ci push"
    git push
    sleep 1200
done
