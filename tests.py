# Enthusiasts, 2015

from transform import *
from load import *
import models
from postgres import *

# TODO: Тесты для отдела тестирования тоже сюда можно писать

# ВАЖНО: Тесты не должны зависеть друг от друга. Серьёзно, лучше просто код копипастить, если есть необходимость.
# По сути всё, кроме пометки integrated - юнит-тесты.

def main_test():
    clear_db()
    #test_transform_dimensions()
    #test_load_dimensions()
    #test_transform_facts()
    #test_load_facts()
    test_integrated_woextract()

# Использовать для очистки тестовой БД.
def clear_db():
    postgres_injection = PostgresInjection()
    with postgres_injection.connection() as connection, connection.cursor() as curs:
        curs.execute("DELETE FROM checkins WHERE 1=1")
        curs.execute("DELETE FROM clients WHERE 1=1")
        curs.execute("DELETE FROM entertainments WHERE 1=1")
        curs.execute("DELETE FROM zones WHERE 1=1")
        curs.execute("DELETE FROM times WHERE 1=1")


def test_load_dimensions():
    postgres_injection = PostgresInjection()

    ents = list(map(lambda x: models.Entertainment("title", 100, "zone_title", 0.0, 0.0, 100, False), range(10)))

    load_dimensions(postgres_injection, [ents, None, None])


def test_transform_facts():
    postgres_injection = PostgresInjection()

    checkins_instagram = list(map(lambda x: {
        INSTA_URL: "http://instagram.com/someurl",
        INSTA_USERNAME: "username",
        INSTA_USER_URL: "http://instagram.com/username_url",
        INSTA_DATETIME: "2015-11-23 01:31:39 UTC",
        INSTA_LONGTITUDE: "0.0",
        INSTA_LATITUDE: "0.0"
    }, range(10)))

    transform_facts(postgres_injection, checkins_instagram)

def test_transform_dimensions():
    postgres_injection = PostgresInjection()

    # Ага, именно тут юзаем чекины в качестве исчтоников пользователей, почему бы и нет.
    checkins_instagram = list(map(lambda x: {
        INSTA_URL: "http://instagram.com/someurl",
        INSTA_USERNAME: "username",
        INSTA_USER_URL: "http://instagram.com/username_url",
        INSTA_DATETIME: "2015-11-23 01:31:39 UTC",
        INSTA_LONGTITUDE: "0.0",
        INSTA_LATITUDE: "0.0"
    }, range(10)))

    transform_dimensions([], checkins_instagram, [], [])

def test_load_facts():
    postgres_injection = PostgresInjection()

    # По сути должно кидать эксепшн, если в базе нет entertainment, client, time с нулевыми айдишниками.
    # Эксепшн типа с ограничением целостности.
    from datetime import datetime
    checkins = list(map(
        lambda x: models.CheckIn("url", datetime.now(), "0.0", "0.0", "username", "http://instagram.com/username"),
        range(10)
    ))

    load_facts(postgres_injection, [checkins])

def test_integrated_woextract():
    postgres_injection = PostgresInjection()

    checkins_instagram = list(map(lambda x: {
        INSTA_URL: "http://instagram.com/someurl",
        INSTA_USERNAME: "username",
        INSTA_USER_URL: "http://instagram.com/username_url",
        INSTA_DATETIME: "2015-11-23 01:31:39 UTC",
        INSTA_LONGTITUDE: "0.0",
        INSTA_LATITUDE: "0.0"
    }, range(1)))

    entertainments_datamosru = list(map(lambda x: {
        ENTERTAINMENTS_TITLE: "title",
        ENTERTAINMENTS_COST: "100",
        ENTERTAINMENTS_LONGITUDE: 0.0,
        ENTERTAINMENTS_LATITUDE: 0.0,
        ENTERTAINMENTS_ZONE_TITLE: "zone_title",
        ENTERTAINMENTS_SEAT_COUNT: 100,
        ENTERTAINMENTS_SOCIAL_PRIVELEGES: False
    }, range(10)))

    zones_datamosru = []

    polygons_nowhere = []

    (ents, clients, zones) = transform_dimensions(entertainments_datamosru, checkins_instagram, zones_datamosru, polygons_nowhere)

    load_dimensions(postgres_injection, [ents, clients, zones])
    facts = transform_facts(postgres_injection, checkins_instagram)
    load_facts(postgres_injection, [facts])

