# Enthusiasts, 2015

import logging
import time

from models import *
from data_consts import *


def transform_dimensions(dimens):
    entertainments_datamosru = dimens[0]
    # TODO: перенести куда-нибудь или запилить в экстракте
    clients_instagram = []
    zones_datamosru = dimens[1]
    # TODO: перенести куда-нибудь или запилить в экстракте
    polygons_nowhere = []
    # TODO: CHECK IT
    # TODO: I'M SERIUSLY
    # Times будет генерироваться в лоаде сразу.

    entertainments = []
    clients = []
    zones = []
    times = []

    # set zones
    try:
        for data in zones_datamosru:
            title = data[ZONE_TITLE]
            timestamp = time.time()  # canonical time
            zones.append(Zone(title, timestamp, None))
    except Exception as e:
        logging.error("Exception in transforming zones data: ", e.args[0])

    # TODO: not working yet
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

    # TODO: not working yet
    # set clients
    try:
        for data in clients_instagram:
            url = data[INSTA_USER_URL]
            title = data[INSTA_USERNAME]
            clients.append(Client(title, url))
    except Exception as e:
        logging.error("Exception in transforming clients data: ", e.args[0])

    # set clients times
    try:
        import dateutil.parser
        for data in clients_instagram:
            datetime = dateutil.parser.parse(data[INSTA_DATETIME])
            times.append(Time(datetime))
    except Exception as e:
        logging.error("Exception in transforming times data: ", e.args[0])

    logging.info("Dimensions transformed.")

    # TODO: Clients не возвращается
    dimens[0] = entertainments
    dimens[1] = zones
    dimens.append(times)


def transform_facts(postgres_injection, facts):
    checkins_instagram = facts[0]
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
                    WHERE year = %s and month=%s and day=%s AND time=%s
                    """,
                    (row.datetime.year, row.datetime.month, row.datetime.day, row.datetime.time())
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

    facts[0] = table
