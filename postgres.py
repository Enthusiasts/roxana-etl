__author__ = 'debal'

import psycopg2


class PostgresInjection(object):
    __dbConfig = dict(dbhost="localhost", dbport=5432, dbname="roxana", dbuser="roxana_consumer", dbpassword="qwerty1234")

    def connection(self):
        return psycopg2.connect(host=self.__dbConfig["dbhost"],
                                port=self.__dbConfig["dbport"],
                                database=self.__dbConfig["dbname"],
                                user=self.__dbConfig["dbuser"],
                                password=self.__dbConfig["dbpassword"])
