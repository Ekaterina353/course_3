import os
from dotenv import load_dotenv
import psycopg2  # Импортируем модуль psycopg2
from psycopg2 import Error  # Импортируем класс Error из psycopg2

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")


class DBManager:
    """Класс для взаимодействия с базой данных"""

    def __init__(self):
        self.__conn = None
        self.__cur = None

    def connect_db(self):
        """Подключение к базе данных"""
        try:
            # Подключаемся к базе данных postgres для создания новой базы
            self.__conn = psycopg2.connect(database=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
            self.__conn.autocommit = True  # Важно для выполнения команд CREATE DATABASE
            self.__cur = self.__conn.cursor()
            print("Успешное подключение к PostgreSQL")  # Вывод для проверки подключения
        except (Exception, Error) as error:
            print("Ошибка при подключении к PostgreSQL", error)
            raise error

    def create_database(self, db_name=DB_NAME):
        """Создание базы данных, если она не существует"""
        try:
            self.__cur.execute(f"CREATE DATABASE {db_name}")
            print(f"База данных {db_name} успешно создана")
        except (Exception, Error) as error:
            print(f"Ошибка при создании базы данных {db_name}", error)
            raise error

    def connect_to_new_db(self, database=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT):
        """Подключение к созданной базе данных"""
        try:
            # Закрываем текущее соединение
            if self.__conn:
                self.__conn.close()
            # Подключаемся к новой базе данных
            self.__conn = psycopg2.connect(database=database, user=user, password=password, host=host, port=port)
            self.__conn.autocommit = True
            self.__cur = self.__conn.cursor()
            print(f"Успешное подключение к базе данных {database}")  # Вывод для проверки подключения
        except (Exception, Error) as error:
            print(f"Ошибка при подключении к базе данных {database}", error)
            raise error

    def create_tables(self):
        """Создание таблиц organizations и vacancies"""
        try:
            self.__cur.execute(
                """
                CREATE TABLE organizations (
                    id serial PRIMARY KEY,
                    name varchar(255) NOT NULL
                );
                CREATE TABLE vacancies (
                    id serial PRIMARY KEY,
                    company_id int REFERENCES organizations(id),
                    vacancy varchar(255) NOT NULL,
                    salary_from int,
                    salary_to int,
                    url text
                );
                """
            )
            self.__conn.commit()  # Подтверждаем создание таблиц
            print("Таблицы organizations и vacancies успешно созданы")
        except (Exception, Error) as error:
            print("Ошибка при создании таблиц", error)
            raise error

    def get_companies_and_vacancies_count(self):
        """Получает список всех компаний и количество вакансий у каждой компании."""
        try:
            self.__cur.execute(
                "SELECT name, COUNT(*) FROM organizations JOIN vacancies on vacancies.company_id = organizations.id GROUP BY name"
            )
            companies = self.__cur.fetchall()
            for company in companies:
                print(company[0], ":", company[1])
        except (Exception, Error) as error:
            raise error

    def get_all_vacancies(self):
        """Получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию"""
        try:
            self.__cur.execute(
                "SELECT c.name AS company_name, v.vacancy, v.salary_from || '-' || v.salary_to AS range_salary, v.url FROM vacancies v JOIN organizations c ON v.company_id = c.id"
            )
            vacancies = self.__cur.fetchall()
            for vacancy in vacancies:
                print(
                    f"Компания: {vacancy[0]}, Название вакансии: {vacancy[1]}, Зарплата: {vacancy[2]}, Ссылка на вакансию: {vacancy[3]}"
                )
        except (Exception, Error) as error:
            raise error

    def get_avg_salary(self):
        """Получает среднюю зарплату по вакансиям"""
        try:
            self.__cur.execute(
                """SELECT (AVG(salary_to) + AVG(salary_from)) / 2 as avg_salary
            FROM vacancies WHERE salary_to > 0 AND salary_from > 0"""
            )
            avg_salary = self.__cur.fetchone()[0]
            print(f"Средняя зарплата: {avg_salary}")
            return avg_salary
        except (Exception, Error) as error:
            raise error

    def get_vacancies_with_higher_salary(self):
        """Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям"""
        try:
            avg_sum = self.get_avg_salary()
            self.__cur.execute(f"SELECT v.vacancy, v.salary_to FROM vacancies v WHERE salary_to > {avg_sum}")
            higher_salaries = self.__cur.fetchall()
            for vacancy in higher_salaries:
                print(f"Название вакансии: {vacancy[0]}, Зарплата: {vacancy[1]}")
        except (Exception, Error) as error:
            raise error

    def get_vacancies_with_keyword(self, keyword):
        """Получает список всех вакансий, в названии которых содержатся переданные в метод слова, например python"""
        try:
            self.__cur.execute("SELECT v.vacancy FROM vacancies v WHERE v.vacancy ILIKE %s", (f"%{keyword}%",))
            vacanies_with_keyword = self.__cur.fetchall()
            for vacancy in vacanies_with_keyword:
                print(f"Название вакансии: {vacancy[0]}")
        except (Exception, Error) as error:
            raise error
