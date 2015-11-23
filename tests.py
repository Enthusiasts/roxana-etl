# Enthusiasts, 2015

from data_consts import *
from extract import *
from transform import *
from load import *
import models
from postgres import *

# TODO: Тесты для отдела тестирования тоже сюда можно писать


def main_test():
    test_load_dimensions()
    test_transform_facts()


def test_load_dimensions():
    postgres_injection = PostgresInjection()

    ents = list(map(lambda x: models.Entertainment("title", 100, "zone_title", 0.0, 0.0, 100, False), range(10)))

    load_dimensions(postgres_injection, ents, None, None)


def test_transform_facts():
    postgres_injection = PostgresInjection()

    checkins = list(map(lambda x: {
        INSTA_URL: "url",
        INSTA_USERNAME: "username",
        INSTA_DATETIME: "21 11 2015",
        INSTA_GEO: "0.0 0.0"
    }, range(10)))

    transform_facts(postgres_injection, checkins)
