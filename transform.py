import logging

from models import *

__author__ = 'someone'


def transform(postgres_injection, data_mos_ru, instagram):
    entertainments = [Entertainment("title", 0, "zone_title", 0.0, 0.0)]
    checkins = [CheckIn()]
    times = [Time()]
    clients = [Client()]
    zones = [Zone()]
    logging.info("Transformed")
    return entertainments, checkins, times, clients, zones
