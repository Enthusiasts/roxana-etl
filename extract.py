# Enthusiasts, 2015

import json
import os
import codecs
from default_raw_paths import *
import logging


def __from(raw_directory):
    filenames = os.listdir(raw_directory)
    files = list(map(lambda x: codecs.open(os.path.join(raw_directory, x), 'r', encoding='utf_8'), filenames))
    jsons = list(map(lambda x: (x.name, json.load(x)), files))
    map(lambda x: x.close(), files)
    return jsons


def extract_dimensions():

    # Явно указываем что где искать
    logging.info("Extract of entertainments started")

    # Добавляет тип заведения исходя из названия файла
    def __add_type_entry(json_ent, name):
        import os
        json_ent.update({"TYPE": os.path.splitext(os.path.basename(name))[0]})
        return json_ent

    from itertools import chain
    ents_data_mos_ru_mapped = [
        list(map(
            lambda t: __add_type_entry(t, name)
            , jsons))
        for x in DEF_PATHS_DIMENSIONS_ENTERTAINMENTS
        for (name, jsons) in __from(x)
    ]

    ents = [list(chain.from_iterable(ents_data_mos_ru_mapped))]

    #logging.info("Extract of zones started")
    #zones = list(chain.from_iterable(list(map(lambda x: (__from(x))[1], DEF_PATHS_DIMENSIONS_ZONES))))

    logging.info("Extract of clients started")
    clients = []
    for path in DEF_PATHS_DIMENSIONS_CLIENTS:
        jsons = __from(path)
        clients.extend(list(map(lambda x: x[1], jsons)))

    #logging.info("Extract of polygons started")
    #pols = list(chain.from_iterable(list(map(lambda x: (__from(x))[1], DEF_PATHS_DIMENSIONS_POLYGONS))))

    return {
        "Entertainments": ents,
        "Zones": [],
        "Clients": clients,
        "Polygons": []
    }


def extract_facts():
    logging.info("Extract of facts started")
    facts = []
    for path in DEF_PATHS_FACTS:
        jsons = __from(path)
        facts.extend(list(map(lambda x: x[1], jsons)))
    return {
        "Checkins": facts
    }
