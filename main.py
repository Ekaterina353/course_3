from src.api import Parser
from src.filter import Filter
from src.interface import DBManager
from src.write_data_in_db import DB

hh = Parser()
data = DBManager()
db = DB()


def main():
    db.connect_db()
    data.connect_db()
    db.create_db()
    vac = hh.api("менеджер")
    fil = Filter(vac)
    vacancies = fil.list_dict()
    db.fill_data(vacancies)
    data.get_companies_and_vacancies_count()
    data.get_all_vacancies()
    data.get_avg_salary()
    data.get_vacancies_with_higher_salary()
    data.get_vacancies_with_keyword("менеджер")


if __name__ == "__main__":
    main()
