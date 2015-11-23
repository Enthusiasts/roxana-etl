# Enthusiasts, 2015

from data_consts import *
from extract import *
from transform import *
from load import *
import models
from postgres import *

# TODO: Тесты для отдела тестирования тоже сюда можно писать


def main_test():
    test_transform_dimensions()
    test_load_dimensions()
    test_transform_facts()
    #test_integrated()


def test_load_dimensions():
    postgres_injection = PostgresInjection()

    ents = list(map(lambda x: models.Entertainment("title", 100, "zone_title", 0.0, 0.0, 100, False), range(10)))

    return load_dimensions(postgres_injection, [ents, None, None])


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

    return transform_facts(postgres_injection, checkins_instagram)

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

    return transform_dimensions([], checkins_instagram, [], [])

def test_integrated():
    postgres_injection = PostgresInjection()

    (ents, clients, zones) = test_transform_dimensions()
    print(ents)
    print(clients)
    print(zones)
    load_dimensions(postgres_injection, [ents, clients, zones])
    facts = test_transform_facts()
    #load_facts(postgres_injection, facts)
