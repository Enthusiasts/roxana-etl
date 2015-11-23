# Enthusiasts, 2015

import json
import os
from default_raw_paths import *


def __from(raw_directory):
    filenames = os.listdir(raw_directory)
    files = list(map(lambda x: open(os.path.join(raw_directory, x), 'r'), filenames))
    jsons = list(map(lambda x: json.load(x), files))
    map(lambda x: x.close(), files)
    return jsons


# TODO: REMOVE THIS
'''# Возвращает json-ы с соответсвующих источников.
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

    return data_mos_ru, instagram, [], []'''


def extract_dimensions():
    # все данные боксятся к список, для удобства обработки внутри transform методов
    result = []
    for direct in DEF_PATHS_DIMENS:
        print("Extract started - dimens: " + direct, flush=True)
        result.append(__from(direct))
        print("Extract finished - dimens: " + direct, flush=True)
    print("All dimens extract stages finished", flush=True)
    return result


# TODO : сделать, когда появится информация
def extract_facts():
    print("de facto no facts. go away")
    return [[{"WTF": "You've been had by Ace Ventura"}]]
