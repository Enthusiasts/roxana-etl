# Enthusiasts, 2015

import logging
import data_consts

# TODO: Закончить обработку


def load_dimensions(postgres_injection, dimens):
    entertainments = dimens[0]
    clients = dimens[1]
    zones = dimens[2]
    times = dimens[3]

    varchar_maxnum = data_consts.VARCHAR_MAXNUMBER

    try:
        # Transaction in curs scope.
        with postgres_injection.connection() as connection, connection.cursor() as curs:
            # TODO: handle on conflict!!!
            # Load entertainments
            if entertainments:
                ent_tuples = list(map(
                    lambda x: (
                        x.global_id, x.title[:varchar_maxnum], x.cost, x.zone_title[:varchar_maxnum], x.longitude,
                        x.latitude, x.seats_count, x.social_priveleges, x.type[:varchar_maxnum]
                    ),
                    entertainments
                ))
                for tuple in ent_tuples:
                    curs.execute("SELECT FROM entertainments WHERE id =%s", (tuple[0],))
                    if curs.rowcount == 0:
                        curs.execute("INSERT INTO entertainments VALUES (%s, %s,%s,%s,%s,%s,%s,%s, %s)", tuple)
                    else:
                        curs.execute("UPDATE entertainments "
                                     "SET title = %s, cost = %s, zone_title = %s,longtitude = %s,"
                                     "latitude = %s, seats_count = %s, social_priveleges = %s,"
                                     "type = %s WHERE id = %s", tuple[1:] + (tuple[0],))

            # Load clients
            if clients:
                client_tuples = list(map(
                    lambda x: (x.title, x.url),
                    clients
                ))
                for tuple in client_tuples:
                    curs.execute("SELECT FROM clients WHERE url =%s", (tuple[1],))
                    if curs.rowcount == 0:
                        curs.execute("INSERT INTO clients VALUES (DEFAULT,%s,%s)", tuple)
                    else:
                        #Клиент с таким url уже существует, думаю, можно не обновлять
                        pass

            # Load zones
            if zones:
                zone_tuples = list(map(
                    lambda x: (x.date_created, x.title, x.polygon),
                    zones
                ))
                curs.executemany("INSERT INTO zones VALUES (%s,%s,%s)", zone_tuples)

            # Load times
            if times:
                def dayoffweek_asrus(day_number):
                    return {
                        0: "Понедельник",
                        1: "Вторник",
                        2: "Среда",
                        3: "Четверг",
                        4: "Пятница",
                        5: "Суббота",
                        6: "Воскресенье"
                    }[day_number]

                times_tuples = list(map(
                    lambda x: (x.datetime.year,
                               x.datetime.month,
                               x.datetime.day,
                               dayoffweek_asrus(x.datetime.weekday()),
                               x.datetime.time()
                               ),
                    times
                ))
                curs.executemany("""
                                 INSERT INTO times (id, year, month, day, dayofweek, time)
                                 VALUES (DEFAULT,%s,%s,%s,%s,%s)
                                 """,
                                 times_tuples)

        logging.info("Dimensions loaded.")

    except Exception as e:
        logging.error("Exception in dimensions loading: " + e.args[0])
        print(e.args[1])


def load_facts(postgres_injection, facts):
    checkins = facts[0]

    try:
        with postgres_injection.connection() as connection, connection.cursor() as curs:
            if checkins:
                checkins_tuples = list(map(
                    lambda x: (x.client_id, x.entertainment_id, x.time_id, x.url, x.longtitude, x.latitude),
                    checkins
                ))

                curs.executemany(
                    """
                    INSERT INTO checkins (client_id, entertainment_id, time_id, url, longtitude, latitude)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """,
                    checkins_tuples
                )

        logging.info("Facts loaded.")

    except Exception as e:
        logging.error("Exception in facts loading: " + e.args[0])