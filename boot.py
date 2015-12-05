# Enthusiasts, 2015

import logging
from extract import *
from transform import *
from load import *
import models
from postgres import *

# True - test mode, False - Work mode
TEST = True


def etl_process(target, postgres_injection):
    if target == TYPE_DIMENS:
        dimens = extract_dimensions()
        (ents, clients, zones, times) = transform_dimensions(dimens)
        load_dimensions(postgres_injection, [ents, clients, zones, times])
    elif target == TYPE_FACTS:
        facts = extract_facts()
        checkins = transform_facts(postgres_injection, facts)
        load_facts(postgres_injection, [checkins])
    else:
        print("Target type is invalid")


# processing function
def main():
    postgres_injection = PostgresInjection()
    etl_process(TYPE_DIMENS, postgres_injection)
    etl_process(TYPE_FACTS, postgres_injection)

# script start
# TODO: Может заменить все принты на логи, все логи на принты, или дублировать одно с другим?
logging.basicConfig(filename="roxana-etl" + ".log", level=logging.DEBUG, format='%(asctime)s %(message)s')

if TEST:
    # В тестах теперь появился метод очистки БД, поэтому тот файлик в продакшн боюсь совать.
    from tests import *
    main_test()
else:
    main()
