import json
import os
import logging

__author__ = 'someone'


def __from(raw_directory):
    filenames = os.listdir(raw_directory)
    files = list(map(lambda x: open(os.path.join(raw_directory, x), 'r'), filenames))
    jsons = list(map(lambda x: json.load(x), files))
    map(lambda x: x.close(), files)
    return jsons


# Возвращает json-ы с соответсвующих источников.
def extract(**kwargs):
    instagram = []
    data_mos_ru = []

    try:
        dir_instagram = kwargs["instagram"]
        dir_data_mos_ru = kwargs["data_mos_ru"]
        instagram = __from(dir_instagram)
        data_mos_ru = __from(dir_data_mos_ru)
        logging.info("Extracted.")

    except KeyError:
        logging.error("Extract: cannot allocate \"instagram\" or \"data_mos_ru\"")

    return data_mos_ru, instagram
