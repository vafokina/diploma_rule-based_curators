# -*- coding: utf-8 -*-
import psycopg2, logging
from psycopg2 import sql
from psycopg2.extras import DictCursor

class DataBaseService:

    SELECT_CURATOR_WITH_ID = "SELECT * FROM curator WHERE id=%s"
    SELECT_CURATORS_WITH_TYPE = "SELECT * FROM curator WHERE type=%s"
    SELECT_OTHER_CURATORS_WITHOUT_TYPE = "SELECT * FROM curator WHERE type<>%s AND id<>%s"
    SELECT_OTHER_CURATORS = "SELECT * FROM curator WHERE id<>%s"
    SELECT_CURATOR_IDS_WITH_FUNCTION = "SELECT curator_id FROM curator_function WHERE function=%s"
    SELECT_ALL_CURATORS = "SELECT * FROM curator"
    INSERT_CURATOR = "INSERT INTO curator (type, state, host, port) VALUES (%s, %s, %s, %s) RETURNING id"
    INSERT_CURATOR_FUNCTION = "INSERT INTO curator_function (curator_id, function) VALUES (%s, %s) RETURNING id"
    DELETE_CURATOR = "DELETE FROM curator WHERE id=%s"
    DELETE_CURATOR_FUNCTION = "DELETE FROM curator_function WHERE curator_id=%s"
    DELETE_ALL_CURATORS = "DELETE FROM curator"
    DELETE_ALL_CURATOR_FUNCTIONS = "DELETE FROM curator_function"
    
    def __init__(self, name, user, password, host, port):
        self.log = logging.getLogger(f"{__name__}.{self.__class__.__name__}",)
        #try:
        self.log.debug("start connection to PostgreSQL")
        self.connection = psycopg2.connect(dbname=name, user=user, 
            password=password, host=host, port=port)
        #self.cursor = self.connection.cursor()
        #except Exception as ex:
        #    self.log.error(str(type(ex)) + " : " + str(ex))

    def __enter__(self):
        return self

    def __exit__(self):
        try:
            self.log.debug("close connection to PostgreSQL")
            #self.cursor.close()
            self.connection.close()
        except Exception as ex:
            self.log.error(str(type(ex)) + " : " + str(ex))

    def select(self, selectQuery, params: tuple):
        self.log.debug("Select sql statement : " + selectQuery + " " + str(params))
        with self.connection.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute(selectQuery, params)
            records = cursor.fetchall()
            self.connection.commit()
            return records

    def insert(self, insertQuery, params: tuple):
        self.log.debug("Insert sql statement : " + insertQuery + " " + str(params))
        with self.connection.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute(insertQuery, params)
            id = cursor.fetchone()[0]
            self.connection.commit()
            return id

    def delete(self, deleteQuery, params: tuple):
        self.log.debug("Delete sql statement : " + deleteQuery + " " + str(params))
        with self.connection.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute(deleteQuery, params)
            self.connection.commit()

    def clear(self):
        self.log.debug("Delete sql statement : " + self.DELETE_ALL_CURATOR_FUNCTIONS)
        with self.connection.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute(self.DELETE_ALL_CURATOR_FUNCTIONS)
            self.connection.commit()
        self.log.debug("Delete sql statement : " + self.DELETE_ALL_CURATORS)
        with self.connection.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute(self.DELETE_ALL_CURATORS)
            self.connection.commit()
            
    