# Tayyip Güney 17.05.2022

# API Exercises

# NeoWs (Near Earth Object Web Service) is a RESTful web service for near earth Asteroid information. 
# With NeoWs a user can: search for Asteroids based on their closest approach date to Earth, 
# lookup a specific Asteroid with its NASA JPL small body id, as well as browse the overall data-set.

# TASK
# Take the asteroid data that poses a potential danger to the world between July 1, 2016, and July 30, 2016, and save it in the astorid.csv file.


import requests
import os
import csv

fileLocation = os.getcwd()

api_key = "l7LiWkmiE89Dr3pjU9pMUo1BOMa032oyfOx5dxfe"
s_date= "" #start date for query
e_date= "" #end date for query

astroid_datas = []

# Finding the start and end dates to pull 7 days of data
for st_d in range(1,31,7): # the api only allows 7 days of data extraction
    
    end_d = st_d+6
    if st_d<10: 
        s_date = f"2016-07-0{st_d}"
    if st_d >= 10:
        s_date = f"2016-07-{st_d}"

    if end_d < 10:
        e_date = f"2016-07-0{end_d}"
    if end_d >= 10 and end_d < 31:
        e_date = f"2016-07-{end_d}"
    if end_d > 30:
        e_date = f"2016-07-30"
# Finding the start and end dates to pull 7 days of data    

# get data from API
    response = requests.get("https://api.nasa.gov/neo/rest/v1/feed",params={
        "start_date" : s_date,
        "end_date" : e_date,
        "api_key" : api_key
    })
# get data from API
   
# We keep the dates between the start and end date in a list
    st_int = int(s_date.split("-")[2]) # convert start date to int
    end_int = int(e_date.split("-")[2]) # convert end date to int
    date_list=[]
    for i in range(st_int,end_int+1):
        if i<10:
            date_list.append(f"2016-07-0{i}")
        else:
            date_list.append(f"2016-07-{i}")
# We keep the dates between the start and end date in a list
    
    for i in date_list: # looping the list of dates to filter
        data_dt = response.json()["near_earth_objects"][i]  # list of dates to filter
        for j in range(len(data_dt)): # looping the length of list
            data_pot = data_dt[j]["is_potentially_hazardous_asteroid"]
            data_all = data_dt[j]
            if data_pot == True: # is it potentially hazardous asteroid ?
                astroid_datas.append(data_all)
                
    date_list.clear()
    
print(len(astroid_datas))
# write to csv file
keys=['links','id','neo_reference_id','name','nasa_jpl_url','absolute_magnitude_h','estimated_diameter','is_potentially_hazardous_asteroid','close_approach_data','is_sentry_object']
with open(f"{fileLocation}\\astroid.csv","w",encoding='UTF8',newline='') as f:
    writer = csv.DictWriter(f,keys)
    writer.writeheader()
    for i in range(len(astroid_datas)):
        writer.writerow(astroid_datas[i])
