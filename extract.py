# Enthusiasts, 2015

import json
import os
import codecs
from default_raw_paths import *
import logging


def __from(raw_directory):
    filenames = os.listdir(raw_directory)
    files = list(map(lambda x: codecs.open(os.path.join(raw_directory, x), 'r', encoding='utf-8'), filenames))
    jsons = list(map(lambda x: (x.name, json.load(x)), files))
    map(lambda x: x.close(), files)
    return jsons

def extract_dimensions():
    # все данные боксятся к список, для удобства обработки внутри transform методов
    '''
    entertainments_datamosru = dimens[0]
    clients_instagram = dimens[1]
    zones_datamosru = dimens[2]
    polygons_nowhere = dimens[3]
    '''
    '''
    result = []
    for direct in DEF_PATHS_DIMENS:
        print("Extract started - dimens: " + direct, flush=True)
        result.append(__from(direct))
        print("Extract finished - dimens: " + direct, flush=True)
    print("All dimens extract stages finished", flush=True)
    return result
    '''

    # Явно указываем что где искать
    logging.info("Extract of entertainments started")

    # Добавляет тип заведения исходя из названия файла
    def __add_type_entry(json_ent, name):
        import os
        json_ent.update({"TYPE": os.path.splitext(os.path.basename(name))[0]})
        return json_ent

    from itertools import chain
    ents_data_mos_ru_mapped = [
        map(
            lambda t: __add_type_entry(t, name)
            , jsons)
        for x in DEF_PATHS_DIMENSIONS_ENTERTAINMENTS
        for (name, jsons) in __from(x)
    ]

    ents = [list(chain.from_iterable(ents_data_mos_ru_mapped))]

    logging.info("Extract of zones started")
    zones = list(chain.from_iterable(map(lambda x: (__from(x))[1], DEF_PATHS_DIMENSIONS_ZONES)))

    logging.info("Extract of clients started")
    clients = list(chain.from_iterable(map(lambda x: (__from(x))[1], DEF_PATHS_DIMENSIONS_CLIENTS)))

    logging.info("Extract of polygons started")
    pols = list(chain.from_iterable(map(lambda x: (__from(x))[1], DEF_PATHS_DIMENSIONS_POLYGONS)))

    return {
        "Entertainments": ents,
        "Zones": zones,
        "Clients": clients,
        "Polygons": pols
    }


def extract_facts():
    logging.info("Extract of facts started")
    facts = list(map(lambda x: (__from(x))[1], DEF_PATHS_FACTS))
    return {
        "Checkins": facts
    }
