#!/usr/bin/env python
# coding: utf-8

# In[1]:


# THIS SCRIPT DOWNLOADS A SNAPSHOT OF THE CURRENT TRAIN DEPARTURES FOR EACH SELECTED TRAINSTART
# RUN THIS SCRIPT A FEW TIMES PER DAY TO CATCH ALL DEPATURES
import warnings
warnings.filterwarnings("ignore", 'This pattern has match groups')

# ADD JUPYTHER PROGRESS BAR
from ipywidgets import IntProgress
from IPython.display import display
import time


# In[2]:


import pandas as pd
stations = pd.read_csv("./generated/0_db_station_lk.csv",sep=';',encoding="utf-8")
stations.head(5)


# In[3]:


# THIS FUNKTION EXTRACTS THE NEEDED INFORMATION FROM THE A JSON RESPONSE

def format_json_from_departureStationBoard_api(_json):
    ret = []
    
    for train in _json:
        train_entry = {}
        
        
        # ALLOW ONLY THE FOLLOWING PRODUCT TYPE
        train_entry['type'] = train['train']['type']
        if train_entry['type'] == "RB" or train_entry['type'] == "RE" or train_entry['type'] == "IC" or train_entry['type'] == "ICE":
            pass
        else:
            continue
        
        
        train_entry['name'] = train['train']['name']
        train_entry['line'] = train['train']['line']
        train_entry['number'] = train['train']['number']
        
        
        train_entry['current_station'] = train['currentStation']['id']
        train_entry['current_station_name'] = train['currentStation']['title']
        train_entry['current_station_departure_time'] = train['departure']['scheduledTime']
        
        stops = ""
        for stop in train['stops']:
            #print(stop)
            stops = stops + str(stop['station']['id'])
            if 'departure' in stop:
                if 'scheduledTime' in stop['departure']:
                    stops = stops + "%" + str(stop['departure']['time'])
                else:
                    stops = stops + "%"
                    
                if 'delay' in stop['departure']:
                    stops = stops + "%" + str(stop['departure']['delay'])
                else:
                    stops = stops + "%"
                    
                    
                    
            stops = stops + ","                
        train_entry['stops'] = stops

        ret.append(train_entry)

    return ret


# In[4]:


# AFTER LOADING THE STATION DATASET WHICH INCLUDES ALL STATIONS WE WANT TO ANALYSE
# THE NEXT STEP IS TO QUERY THE API FOR THE DEPATURES OF THE TRAINS AT THE SELECTED STATION
# THE RESULT SHOULD BE A LIST OF TRAINS AND THEIR DEPARTMENT STATION

import requests
import json
import time

# ALL RESULTS WILL BE STORED IN THE successful_fetch ARRAY EACH FAILED REQUEST IN failed_fetch
failed_fetch = []
successful_fetch = []

def fetch_depature_table(_station_id, _time):
    global failed_fetch
    global successful_fetch
    
    if _time is None:
        r = requests.get('https://marudor.de/api/hafas/v2/departureStationBoard?station='+str(fetch_station_id)+'&profile=db')
    else:
        r = requests.get('https://marudor.de/api/hafas/v2/departureStationBoard?station='+str(fetch_station_id)+'&profile=db,date=' + str(_time))
        
    if r.status_code == 200:
        for fr in format_json_from_departureStationBoard_api(r.json()):
            successful_fetch.append(fr)
    else:
        failed_fetch.append(fetch_station_id)


# In[5]:


# FINALLY START DOWNLOADING ALL DEPATURES FOR EACH LOADED STATION


# In[ ]:


stationd_id = stations['db_station_id']

# PROGRESS BAR INIT
f = IntProgress(min=0, max=len(stationd_id)) # instantiate the bar
display(f) # display the bar

# FETCH EACH STATION
for station in stationd_id:
    #print(station)
    fetch_station_id = station
    fetch_station_time = None #"2021-11-25T8:00:00.000Z"
    fetch_depature_table(fetch_station_id,fetch_station_time)
    
    f.value += 1 
    
    


# In[ ]:





# In[ ]:


# SAVE RESULTS AS CSV
## UGLY !!
# TRANSFROM FETCH RESULT INTO PD COMPATIBLE DATA
_type = []
_name = []
_line = []
_number = []
_current_station = []
_stops = []
_max_capacity = []
_current_station_name = []
_current_station_departure_time = []

for res in successful_fetch:
    et = None
    try:
        et = res[0]
    except:
        et = res
    
    if et is None or len(et) <= 0:
        continue
    #print(et)
    _type.append(et['type'])
    _name.append(et['name'])
    _line.append(et['line'])
    _number.append(et['number'])
    _current_station.append(et['current_station'])
    _current_station_name.append(et['current_station_name'])
    _current_station_departure_time.append(et['current_station_departure_time'])
    _stops.append(et['stops'])
    
    
    # ADD A ESTIMATED CAPACITY
    if et['type'] == "ICE":
        _max_capacity.append(720)
    elif et['type'] == "IC" or et['type'] == "EC":
        _max_capacity.append(468)
    elif et['type'] == "RE":
        _max_capacity.append(602)
    elif et['type'] == "RB":
        _max_capacity.append(426)


fetched_depatures = pd.DataFrame(data={'current_station_departure_time':_current_station_departure_time, 'current_station_name':_current_station_name,'type':_type,'name':_name,'line':_line,'number':_number,'current_station':_current_station,'stops':_stops, 'max_capacity':_max_capacity})
fetched_depatures.head(5)


# In[ ]:


import calendar;
import time;
ts = calendar.timegm(time.gmtime())
print(ts)

fetched_depatures.to_csv("./generated/departure_tables_raw/1_departures_table_"+str(ts)+".csv",sep=';',encoding="utf-8",index=False)


# In[ ]:





# In[ ]:




