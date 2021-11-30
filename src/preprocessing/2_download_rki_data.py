#!/usr/bin/env python
# coding: utf-8

# In[1]:


# TODO
# DOWNLOAD RKI DATA FOR EACH WEEK
# LK FLÄLL 7 TAGE BETROFFENEN RATE DATUM
# ONLY USED LANDKREIS IDS
# SAVE AS CSV


# In[2]:


import warnings
warnings.filterwarnings("ignore", 'This pattern has match groups')


# In[3]:


# IMPORT CSV WHICH CONTAINS THE LANDKREISNAMEN
import pandas as pd

#IMPORTANT TO SET THE TYPE OF ALL COLUMNS TO TYPE STRING str
# TO AVOID BUGS LATER BY DICT ACCESS
used_lk = pd.read_csv("./generated/0_db_station_lk.csv",sep=';',encoding="utf-8",dtype = str)


# IN THIS CASE WE ONLY USING THE LANDKREISE COLUMN
used_lk = used_lk[['rki_ags']]
used_lk.head(5)


# In[4]:


import requests

district_data = None
def fetch_district_data():
    global failed_fetch
    global successful_fetch
    # DOCKER CONTAINER LINK ADRESS TO marlon360/rki-covid-server:v2
    r = requests.get('http://rkiapi:3000/districts')

    if r.status_code == 200:
        return r.json()
    else:
        return None


# In[5]:


district_data = fetch_district_data()
if district_data is None:
    raise Exception('district_data is None so fetch failed')
if not "data" in district_data:
    raise Exception('district_data has no data attribute')
district_data = district_data['data']


# In[6]:


## SAVE ONLY IMPORTANT VALUES
not_found_lk = 0
total_lk = 0


_rki_ags = []
_population = []
_incidence = []
_cases_100k = []
_cases_week = []


for lkags in used_lk['rki_ags']:
    total_lk = total_lk + 1
    #print(lkags)
    if str(lkags) in district_data:
        entry = district_data[str(lkags)]
        _rki_ags.append(lkags)
        _population.append(entry['population'])
        _incidence.append(entry['weekIncidence'])
        _cases_100k.append(entry['casesPer100k'])
        _cases_week.append(entry['casesPerWeek'])

    else:
        not_found_lk = not_found_lk + 1

print(f"missing lk {not_found_lk} from {total_lk} requested")


# In[7]:


## CONVERT TO PANDAS DATAFRAME
fetched_cases = pd.DataFrame(data={'rki_ags':_rki_ags,'population':_population,'incidence':_incidence,'cases_100k':_cases_100k,'cases_week':_cases_week})
fetched_cases.head(5)


# In[8]:


# SAVE RESULT
import calendar;
import time;
ts = calendar.timegm(time.gmtime())
print(ts)

fetched_cases.to_csv("./generated/corona_histroy/cases_"+str(ts)+".csv",sep=';',encoding="utf-8",index=False)


# In[ ]:




