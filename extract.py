import json
import os
import logging

__author__ = 'someone'

'''
Нвдо то же самое, только для разных источников
def extract(raw_directory):
    filenames = os.listdir(raw_directory)
    files = list(map(lambda x: open(x, 'r'), filenames))
    jsons = list(map(lambda x: json.load(x)))
    map(lambda x: x.close(), files)
    return jsons
'''

# Возвращает json-ы с соответсвующих источников.
def extract(**kwargs):
    # if kwargs["dir_checkins"]
    instagram = []
    data_mos_ru = []
    logging.info("Extracted.")
    return data_mos_ru, instagram
