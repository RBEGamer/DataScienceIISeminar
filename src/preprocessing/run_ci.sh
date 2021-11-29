#!/bin/bash

docker-compose up -d
docker exec jupyterds2 jupyter nbconvert --execute --to notebook /home/jovyan/work/1_download_train_schedule.ipynb
docker-compose down
ls -la ./generated/departure_tables_raw
git add ./generated/departure_tables_raw