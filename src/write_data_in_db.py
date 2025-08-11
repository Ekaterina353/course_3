import os
from typing import List

import psycopg2
from psycopg2 import Error

from dotenv import load_dotenv

load_dotenv()

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")


class DB:
    """Класс создания и заполнения таблиц в базе данных"""

    def __init__(self):
        self.__conn = None
        self.__cur = None

    def connect_db(self) -> None:
        """Подключение к базам данных"""
        try:
            self.__conn = psycopg2.connect(
                database=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT
            )
            self.__conn.set_session(autocommit=True)
            self.__cur = self.__conn.cursor()

        except (Exception, Error) as error:
            raise error

    def create_db(self) -> None:
        """Создаем таблицы данных"""
        try:
            self.__cur.execute(
                """CREATE TABLE IF NOT EXISTS organizations (
                id SERIAL PRIMARY KEY,
                name VARCHAR 
            )"""
            )

            self.__cur.execute(
                """CREATE TABLE IF NOT EXISTS vacancies (
                id SERIAL PRIMARY KEY,
                city VARCHAR,
                company_id int REFERENCES organizations(id),
                salary_from int,
                salary_to int,
                url VARCHAR,
                requirements TEXT,
                vacancy VARCHAR
            )"""
            )

        except (Exception, Error) as error:
            raise error

    def find_com(self, name: str) -> int:
        """Возвращает id"""
        self.__cur.execute(f"""SELECT id FROM organizations WHERE name = '{name}'""")
        id_ = self.__cur.fetchone()
        if not id_:
            self.__cur.execute(f"""INSERT INTO organizations (name) VALUES ('{name}') RETURNING id""")
            id_ = self.__cur.fetchone()
        return id_[0]

    def fill_data(self, list_v: List) -> None:
        """Заполнение таблиц"""
        try:

            for vac in list_v:
                id_ = self.find_com(vac["company"])
                self.__cur.execute(
                    """INSERT INTO vacancies
                     (
                         city, 
                         company_id, 
                         salary_from, 
                         salary_to, 
                         url, 
                         requirements, 
                         vacancy
                     )
                     VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                    (
                        vac["city"],
                        id_,
                        vac["salary_from"],
                        vac["salary_to"],
                        vac["url"],
                        vac["requirements"],
                        vac["vacancy"],
                    ),
                )
        except (Exception, Error) as error:
            raise error
