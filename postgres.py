import psycopg2

class PostgresInjection(object):
    __dbConfig = dict(dbhost="localhost", dbport=5432, dbname="postgres", dbuser="postgres", dbpassword="")

    def connection(self):
        return psycopg2.connect(host=self.__dbConfig["dbhost"],
                                port=self.__dbConfig["dbport"],
                                database=self.__dbConfig["dbname"],
                                user=self.__dbConfig["dbuser"],
                                password=self.__dbConfig["dbpassword"])
