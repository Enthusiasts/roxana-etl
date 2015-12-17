# Enthusiasts, 2015

import psycopg2


class PostgresInjection(object):
    __dbConfig = dict(dbhost="192.168.182.128", dbport=5432, dbname="roxana", dbuser="roxana_consumer", dbpassword="qwerty1234")

    def connection(self):
        return psycopg2.connect(host=self.__dbConfig["dbhost"],
                                port=self.__dbConfig["dbport"],
                                database=self.__dbConfig["dbname"],
                                user=self.__dbConfig["dbuser"],
                                password=self.__dbConfig["dbpassword"])
