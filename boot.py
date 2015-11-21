import os
import logging

from extract import extract
from transform import transform
from load import load
from postgres import PostgresInjection

__author__ = 'debalid'


logging.basicConfig(filename="roxana-etl" + ".log", level=logging.DEBUG, format='%(asctime)s %(message)s')

postgres_injection = PostgresInjection()

(json_data_mos_ru, json_instagram, json_entertainments, json_polygons) = extract(data_mos_ru=os.path.join(os.getcwd(), "raw/data_mos_ru"),
                                             instagram=os.path.join(os.getcwd(), "raw/instagram"))

(entertainments, checkins, times, clients, zones) = transform(json_data_mos_ru, json_instagram, json_entertainments, json_polygons)

load(postgres_injection, entertainments, checkins, times, clients, zones)

