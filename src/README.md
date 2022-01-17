# SRC


Start the docker-stack which includes all important services.

* jupyther notebook
* redis-database
* visualisation server
* instance of rki-covid-api
* flask file distribution server


```bash
$ docker-compose up -d
```


After startup you can visit the following endpoints:

* `http://127.0.0.1:9096` => JUPYTHER NOTEBOOK
* `http://127.0.0.1:9095` => RKI API
* `http://127.0.0.1:9097` => FILE SERVER
* `http://127.0.0.1:9098` => VISUALISATION SERVER




# NOTEBOOK

This jupyther notebook generates and downloads the basic datasets
* Corona Dataset Histroy
* DB Depatures
* Community Lists
* Community GEOJSON


The process is split up into the following jupyther notebooks:

## 0_data_preperation

This notebook takes the files from the `./datasets` folder and extracts the following information:

* filter db station data
* convert db station location + rki district data into one geojson file
* generate station lookup tables for frontend
* create custom db station feature geojson
## 1_download_train_schedule

This notebook downloads the train depature tables from each station of interest.
The result ist stored in `./generated/depature_tables_raw`.

## 2_download_rki_data

This notebook downloads the current RKI Covid District data.
It uses the `https://github.com/marlon360/rki-covid-api` docker container to perform this task.
The results are stored in `./generated/corona_history`



## 4_preprocess_for_simulation

Finally this notebook combines all these Data into one dataset
* DB station + community names
* matching of rki_ags with db_station_id by using their coorinates
* combine departure tables (x per day) into one per day
* Trains departures for each station
* list of stations with rki data
* list of departures per train and station

All generated raw files are located in the `generated` folder.
It also generated several helper datasets and lookuptables needed for the frontend.

# VISUALISATION SERVER

Finally the results are showes in an realtime, interactive website.
This nodejs webapp is located in the `./visualisation_server` directory.
Its important to run all! notebooks before starting the server.
For further information please see the README.md in `./visualisation_server`.