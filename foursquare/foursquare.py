import json
from datetime import datetime, timedelta
import psycopg2
from get_price_api import *

import os, codecs

import time, logging

finish_date = datetime.now()
start_date = finish_date + timedelta(days=-1)

finish_date_tms = time.mktime(finish_date.timetuple())
start_date_tms = time.mktime(start_date.timetuple())

dict_list = []

min_timestamp = start_date_tms
max_timestamp = finish_date_tms


def get_dict(data, cost):
    lon, lat, title = data
    result = {
        "lat": lat,
        "lon": lon,
        "title": title,
        "cost": cost
    }
    return result


conf = json.load(codecs.open("config.json", "r", encoding="UTF-8"))
id = conf["fsquare"]["id"]   # TODO : Authdata to config
limit = conf["fsquare"]["limit"]
limit = 2500  # TODO : remove it after add data to config
__db_config = conf["database"]

points = []
with psycopg2.connect(host=__db_config["host"],
                      port=__db_config["port"],
                      database=__db_config["database"],
                      user=__db_config["user"],
                      password=__db_config["password"]) as connect, connect.cursor() as curs:
    curs.execute("SELECT longitude, latitude, title FROM entertainments WHERE cost=0 OFFSET %s LIMIT %s", (id * limit, limit))
    if curs.rowcount > 0:
        points = curs.fetchall()
print(len(points))
points = set(points)
print(len(points))

i = 0
print("Start loading for " + str(len(points)) + " points... Time is " + datetime.now().isoformat())
print("From " + str(id * limit))
print("To " + str((id+1) * limit))
'''for (lon, lat, title) in points:
    get_data(title, lon, lat)
    i += 1
    print(i)'''
costs = get_costs_info(points)
for i in range(len(costs)):
    dict_list.append(get_dict(points[i], costs[i]))


output_json = conf["fsquare"]["output_json"]
try:
    os.remove(output_json)
except Exception as e:
    print("error")

output_file = codecs.open(output_json, "w", encoding = "UTF-8")
output_file.write(json.dumps(dict_list))
output_file.close()

print("Finished. Time is " + datetime.now().isoformat())
