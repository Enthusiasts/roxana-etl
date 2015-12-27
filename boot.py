# Enthusiasts, 2015

import logging
from extract import *
from transform import *
from load import *
import models
from postgres import *
from clusterize import *

# True - test mode, False - Work mode
TEST = False


# processing function
def main():
    postgres_injection = PostgresInjection()

    dimens = extract_dimensions()
    (ents, clients, zones, times) = transform_dimensions(dimens)
    load_dimensions(postgres_injection, [ents, clients, zones, times])

    facts = extract_facts()
    checkins = transform_facts(postgres_injection, facts)
    load_facts(postgres_injection, [checkins])

    cluster_checkins(postgres_injection)


logging.basicConfig(filename="roxana-etl" + ".log", level=logging.DEBUG, format='%(asctime)s %(message)s')
logging.info("======================")

if TEST:
    # В тестах теперь появился метод очистки БД, поэтому тот файлик в продакшн боюсь совать.
    from tests import *
    main_test()
else:
    main()
