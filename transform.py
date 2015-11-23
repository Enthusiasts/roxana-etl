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
            url = data[INSTA_USER_URL]
            title = data[INSTA_USERNAME]
            clients.append(Client(title, url))
    except Exception as e:
        logging.error("Exception in transforming clients data: ", e.args[0])

    return entertainments, clients, zones


def transform_facts(postgres_injection, checkins_instagram):
    # Здесь будут маппинг к entertainments по геопозиции, к times по времени, к clients по юзернейму.
    # Construct big table base
    table = []
    try:
        for data in checkins_instagram:
            url = data[INSTA_URL]
            username = data[INSTA_USERNAME]
            import dateutil.parser
            datetime = dateutil.parser.parse(data[INSTA_DATETIME])
            username_url=data[INSTA_USER_URL]
            lon = data[INSTA_LONGTITUDE]
            lat = data[INSTA_LATITUDE]
            table.append(CheckIn(url, datetime, lon, lat, username, username_url))

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

    return table
