#!/bin/bash

docker-compose up -d jupyterds2
docker exec jupyterds2 jupyter nbconvert --execute --to notebook /home/jovyan/work/1_download_train_schedule.ipynb
docker-compose down jupyterds2
ls -la ./generated/departure_tables_raw
git pull
git add ./generated/departure_tables_raw