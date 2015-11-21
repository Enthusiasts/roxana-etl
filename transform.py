import logging
import time

from models import *
from data_consts import *


# where to find entertainments?
def transform(postgres_injection, data_mos_ru, instagram, entertainments_data, polygons):
    entertainments = []
    checkins = []
    times = []
    clients = []
    zones = []

    # set zones
    try:
        for data in data_mos_ru:
            title = data[ZONE_TITLE]
            timestamp = time.time()  # canonical time
            zones.append(Zone(title, timestamp, None))
    except Exception as e:
        print("Exception in transforming zones data: ", e)

    # set entertainments
    try:
        # verify this code after finishing developing extracting entertainments data
        for i in len(entertainments_data):
            title = entertainments_data[i][ENTERTAINMENTS_ZONE_TITLE]
            cost = entertainments_data[i][ENTERTAINMENTS_COST]
            zone_title = entertainments_data[i][ENTERTAINMENTS_ZONE_TITLE]
            lon = entertainments_data[i][ENTERTAINMENTS_LONGITUDE]
            lat = entertainments_data[i][ENTERTAINMENTS_LATITUDE]
            entertainments.append(Entertainment(i, title, cost, zone_title, lon, lat))
    except Exception as e:
        print("Exception in transforming entertainments data: ", e)

    # set polygons to zone
    try:
        for data in polygons:
            title = data[POLYGONS_TITLE]
            poly = data[POLYGONS_DATA]
            injected = False
            for zn in zones:
                if zn.title == title:
                    # set polygon
                    zn.polygon = poly
                    injected = True
                    break
            if not injected:
                # update polygon if such zone exist
                zones.append(Zone(title, None, poly))
    except Exception as e:
        print("Exception in transforming polygons data: ", e)

    # set clients and checkins
    try:
        for data in instagram:
            # verify this code after finishing developing extracting data from instagram

            url = data[INSTA_URL]
            title = data[INSTA_TITLE]
            founded_client = False
            for client in clients:
                if client.url == url:
                    founded_client = True
                    cl_id = client.id
                    break
            if not founded_client:
                cl_id = len(clients)
                client.append(Client(cl_id, title, url))

            idt = data[INSTA_DATETIME]  # transform it to target format
            day = 42  # get from idt
            month = 4815162342  # get from idt
            year = 2033 # get from idt
            founded_times = False
            for dt in times:
                if dt.year == year and dt.month == month and dt.day == day:
                    times_id = dt.id
                    founded_times = True
                    break
            if not founded_times:
                times_id = len(times)
                day_of_week = "I HATE MONDAYS"  # get from idt
                times.append(Time(times_id, year, month, day, day_of_week))

            geo = data[INSTA_GEO]
            lon = 0.0  # get from geo
            lat = 8.8  # get from geo
            founded_ent = False
            for ent in entertainments:
                if abs(ent.longitude - lon) < GEO_EPSILON and abs(ent.latitude - lat) < GEO_EPSILON:
                    ent_id = ent.id
                    founded_ent = True
                    break
            if not founded_ent:
                ent_id = None

            founded_check = False
            for che in checkins:
                if che.client_id == cl_id and che.entertainment_id == ent_id and che.time_id == times_id:
                    founded_check = True
                    break
            if not founded_check:
                tm = "12:00:37"  # get from idt and set in right format
                checkins.append(cl_id, ent_id, times_id, url, tm, lon, lat)
    except Exception as e:
        print("Exception in transforming clients data: ", e)

    logging.info("Transforming finished")
    # set unique ids to clients at load stage.
    # Maybe it's useful to get id's straight from existing OLAP cube at transform stage?
    return entertainments, checkins, times, clients, zones
