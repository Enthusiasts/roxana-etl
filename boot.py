# Enthusiasts, 2015

from tests import *

# True - test mode, False - Work mode
TEST = True


# TODO: выпилить после прописывания входных параметров функции etl
def old_main():
    '''(json_data_mos_ru, json_instagram, json_entertainments, json_polygons) = extract(data_mos_ru=os.path.join(os.getcwd(), "raw/data_mos_ru"),
                                                 instagram=os.path.join(os.getcwd(), "raw/instagram"))

    (entertainments, checkins, times, clients, zones) = transform(json_data_mos_ru, json_instagram, json_entertainments, json_polygons)

    load(postgres_injection, entertainments, checkins, times, clients, zones)
    '''


# TODO: прописать все необходимые входные пареметры функциям
def etl_process(target):
    if target == TYPE_DIMENS:
        dimens = extract('''do here''')
        transform_dimensions(dimens)
        load_dimensions(dimens)
    elif(target == TYPE_FACTS):
        facts = extract('''do here''')
        transform_facts(facts)
        load_facts(facts)
    else:
        print("Target type is invalid")


# tests function
def test():
    test_load_dimensions()
    test_transform_facts()


# processing function
def main():
    etl_process(TYPE_DIMENS)
    etl_process(TYPE_DIMENS)

# script start
logging.basicConfig(filename="roxana-etl" + ".log", level=logging.DEBUG, format='%(asctime)s %(message)s')

if TEST:
    test()
else:
    main()
