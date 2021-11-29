#!/bin/bash
docker-compose up -d jupyterds2
# DOWNLOAD TRAINDATA
docker exec jupyterds2 jupyter nbconvert --inplace --execute --to notebook /home/jovyan/work/1_download_train_schedule.ipynb
# DOWNLOAD COVID DATA
docker exec jupyterds2 jupyter nbconvert --inplace --execute --to notebook /home/jovyan/work/2_download_rki_data.ipynb
# PREPROCESS DATA = TRAIN + COVID
docker exec jupyterds2 jupyter nbconvert --inplace --execute --to notebook /home/jovyan/work/4_preprocess_for_simulation.ipynb

# PUSH RESULTS
#docker-compose down jupyterds2
ls -la ./generated/departure_tables_raw
git add ./generated/