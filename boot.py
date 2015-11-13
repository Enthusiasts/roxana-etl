import os
import logging

from extract import extract
from transform import transform
from load import load

__author__ = 'debalid'


logging.basicConfig(filename="roxana-etl" + ".log", level=logging.DEBUG, format='%(asctime)s %(message)s')

(json_data_mos_ru, json_instagram) = extract(dir=os.path.join(os.getcwd(), "/raw/"))

(entertainments, checkins, times, clients, zones) = transform(json_data_mos_ru, json_instagram)

load(entertainments, checkins, times, clients, zones)
