import os
import logging

from extract import extract
from transform import *
from load import *
from postgres import PostgresInjection
import models

__author__ = 'debalid'

logging.basicConfig(filename="roxana-etl" + ".log", level=logging.DEBUG, format='%(asctime)s %(message)s')


def old_main():
    '''(json_data_mos_ru, json_instagram, json_entertainments, json_polygons) = extract(data_mos_ru=os.path.join(os.getcwd(), "raw/data_mos_ru"),
                                                 instagram=os.path.join(os.getcwd(), "raw/instagram"))

    (entertainments, checkins, times, clients, zones) = transform(json_data_mos_ru, json_instagram, json_entertainments, json_polygons)

    load(postgres_injection, entertainments, checkins, times, clients, zones)
    '''


def main():
    pass


def test_load_dimensions():
    postgres_injection = PostgresInjection()

    ents = list(map(lambda x: models.Entertainment("title", 100, "zone_title", 0.0, 0.0, 100, False), range(10)))

    load_dimensions(postgres_injection, ents, None, None)


def test_transform_facts():
    postgres_injection = PostgresInjection()

    from datetime import datetime
    checkins = list(map(lambda x: {
        INSTA_URL: "url",
        INSTA_USERNAME: "username",
        INSTA_DATETIME: "21 11 2015",
        INSTA_GEO: "0.0 0.0"
    }, range(10)))

    transform_facts(postgres_injection, checkins)

#test_load_dimensions()
test_transform_facts()

#main()
