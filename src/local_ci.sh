#!/bin/bash
while true
do
    docker-compose up -d jupyterds2
    docker exec jupyterds2 jupyter nbconvert --inplace --execute --to notebook /home/jovyan/work/1_download_train_schedule.ipynb
    docker exec jupyterds2 jupyter nbconvert --inplace --execute --to notebook /home/jovyan/work/2_download_rki_data.ipynb
    docker exec jupyterds2 jupyter nbconvert --inplace --execute --to notebook /home/jovyan/work/4_preprocess_for_simulation.ipynb
    sleep 1200
done