# Enthusiasts, 2015

import logging

# TODO: Закончить обработку


def load_dimensions(postgres_injection, dimens):
    entertainments = dimens[0]
    clients = dimens[1]
    zones = dimens[2]

    try:
        # Transaction in curs scope.
        with postgres_injection.connection() as connection, connection.cursor() as curs:
            # TODO: handle on conflict!!!
            # Load entertainments
            if entertainments:
                ent_tuples = list(map(
                    lambda x: (
                        x.title, x.cost, x.zone_title, x.longitude, x.latitude, x.seats_count, x.social_priveleges
                    ),
                    entertainments
                ))
                curs.executemany("INSERT INTO entertainments VALUES (DEFAULT, %s,%s,%s,%s,%s,%s,%s)", ent_tuples)

            # Load clients
            if clients:
                client_tuples = list(map(
                    lambda x: (x.title, x.url),
                    clients
                ))
                curs.executemany("INSERT INTO clients VALUES (DEFAULT,%s,%s)", client_tuples)

            # Load zones
            if zones:
                zone_tuples = list(map(
                    lambda x: (x.date_created, x.title, x.polygon),
                    zones
                ))
                curs.executemany("INSERT INTO zones VALUES (%s,%s,%s)", zone_tuples)

            # Updating times
            from datetime import date, timedelta
            curs.execute("SELECT year, month, day, dayofweek FROM times ORDER BY id DESC LIMIT 1")
            days_range = []
            if curs.rowcount > 0:
                (year, month, day, dayofweek) = curs.fetchone()
                lastday = date(year, month, day)
                today = date.today()
                delta = today - lastday
                days_range = list((lastday + timedelta(days=x) for x in range(1, delta.days + 1)))
            else:
                days_range = [date.today()]

            if days_range:
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

                days_tuples = list(map(
                    lambda x: (x.year, x.month, x.day, dayoffweek_asrus(x.weekday())),
                    days_range
                ))
                curs.executemany(
                    "INSERT INTO times (id, year, month, day, dayofweek) VALUES (DEFAULT,%s,%s,%s,%s)",
                    days_tuples
                )

        logging.info("Dimensions loaded.")

    except Exception as e:
        logging.error("Exception in load: " + e.args[0])


# TODO : сделать, когда появится информация
# TODO: информация появилась, надо сделать
def load_facts(postgres_injection, checkins):
    print("de facto no facts. nothing to load")
