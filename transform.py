import logging
import time

from models import *
from data_consts import *


def transform_dimensions(entertainments_datamosru, clients_instagram, zones_datamosru, polygons_nowhere):
    # TODO: CHECK IT
    # TODO: I'M SERIUSLY
    # Times будет генерироваться в лоаде сразу.

    entertainments = []
    clients = []
    zones = []

    # set zones
    try:
        for data in zones_datamosru:
            title = data[ZONE_TITLE]
            timestamp = time.time()  # canonical time
            zones.append(Zone(title, timestamp, None))
    except Exception as e:
        logging.error("Exception in transforming zones data: ", e.args[0])

    # set polygons to zone
    try:
        for data in polygons_nowhere:
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
        logging.error("Exception in transforming polygons data: ", e.args[0])

    # set entertainments
    try:
        # verify this code after finishing developing extracting entertainments data
        for i in range(0, len(entertainments_datamosru)):
            title = entertainments_datamosru[i][ENTERTAINMENTS_ZONE_TITLE]
            cost = entertainments_datamosru[i][ENTERTAINMENTS_COST]
            zone_title = entertainments_datamosru[i][ENTERTAINMENTS_ZONE_TITLE]
            lon = entertainments_datamosru[i][ENTERTAINMENTS_LONGITUDE]
            lat = entertainments_datamosru[i][ENTERTAINMENTS_LATITUDE]
            seat = entertainments_datamosru[i][ENTERTAINMENTS_SEAT_COUNT]
            social = entertainments_datamosru[i][ENTERTAINMENTS_SOCIAL_PRIVELEGES]
            entertainments.append(Entertainment(title, cost, zone_title, lon, lat, seat, social))
    except Exception as e:
        logging.error("Exception in transforming entertainments data: ", e.args[0])

    try:
        for data in clients_instagram:
            url = data[INSTA_URL]
            title = data[INSTA_TITLE]
            founded_client = False
            clients.append(Client(title, url))
    except Exception as e:
        logging.error("Exception in transforming clients data: ", e.args[0])


def transform_facts(postgres_injection, checkins_instagram):
    # Здесь будут маппинг к entertainments по геопозиции, к times по времени, к clients по юзернейму.
    try:
        # Construct big table base
        # TODO: IMPLEMENT BIG TABLE!!!
        table = []
        for data in checkins_instagram:
            # TODO: change to real format
            # TODO: REWRITE THIS
            # TODO: SERIOUSLY I BROKE IT
            url = data[INSTA_URL]
            username = data[INSTA_USERNAME]
            idt = data[INSTA_DATETIME]
            '''from datetime import datetime
            from time import mktime
            idt = datetime.fromtimestamp(mktime(time.strptime(idt, "%d %m %y")))'''
            from datetime import datetime
            idt = datetime.now()
            geo = data[INSTA_GEO]
            username_url="username_url"
            lon = 0.0  # get from geo
            lat = 8.8  # get from geo
            table.append(CheckIn(url, idt, lon, lat, username, username_url))

        # Mapping to existing entities
        with postgres_injection.connection() as connection, connection.cursor() as curs:
            for row in table:
                # Map entertainment
                curs.execute(
                    """
                    SELECT id
                    FROM entertainments
                    WHERE abs(longtitude - %s) < %s and abs(latitude - %s) < %s
                    """,
                    (str(row.longtitude), str(GEO_EPSILON), str(row.latitude), str(GEO_EPSILON))
                )
                if curs.rowcount > 0:
                    ent_id = curs.fetchone()
                    row.entertainment_id = ent_id
                else:
                    logging.info(
                        "Cannot find an entertainment for checkin: " +
                        row.url + " (" + str(row.longtitude) + ", " + str(row.latitude) + ")"
                    )

                # Map client
                curs.execute(
                    """
                    SELECT id, url
                    FROM clients
                    WHERE url=%s
                    """,
                    (row.username_url,)  # Must be a tuple
                )
                if curs.rowcount > 0:
                    (cli_id, cli_url) = curs.fetchone()
                    row.client_id = cli_id
                else:
                    logging.info(
                        "Cannot find a client for checkin: " +
                        row.url + " (" + str(row.longtitude) + ", " + str(row.latitude) + ")"
                    )

                # Map time

                curs.execute(
                    """
                    SELECT id
                    FROM times
                    WHERE year = %s and month=%s and day=%s
                    """,
                    (row.datetime.year, row.datetime.month, row.datetime.day)
                )
                if curs.rowcount > 0:
                    time_id = curs.fetchone()
                    row.time_id = time_id
                else:
                    logging.info(
                        "Cannot find a client for checkin: " +
                        row.url + " (" + str(row.longtitude) + ", " + str(row.latitude) + ")"
                    )

        logging.info("Facts transformed.")

    except Exception as e:
        logging.error("Exception in facts transform: " + e.args[0])
        import traceback
        traceback.print_exc()


# TODO: удалить все. методы вызываются из boot.py
# where to find entertainments?
def transform(postgres_injection, data_mos_ru, instagram, entertainments_data, polygons):
    entertainments = []
    checkins = []
    times = []
    clients = []
    zones = []

    '''
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
    '''

    # set clients and checkins
    try:
        for data in instagram:
            # verify this code after finishing developing extracting data from instagram
            '''
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
            '''
            '''
            idt = data[INSTA_DATETIME]  # transform it to target format
            day = 42  # get from idt
            month = 4815162342  # get from idt
            year = 2033  # get from idt
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
            '''

            '''
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
            '''
    except Exception as e:
        print("Exception in transforming clients data: ", e)

    logging.info("Transforming finished")
    # set unique ids to clients at load stage.
    # Maybe it's useful to get id's straight from existing OLAP cube at transform stage?
    return entertainments, checkins, times, clients, zones
