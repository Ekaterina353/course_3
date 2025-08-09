from typing import List
from funcy import get_in


class Filter:
    """Класс для фильтрации данных с hh.ru"""

    def __init__(self, data):
        self.data = data

    def list_dict(self, item=None, dict_vacancies=None, list_vac=None) -> List:
        """Метод для преобразования данных"""

        dict_vacancies["company"] = get_in(item, ["employer", "name"], "не указана компания")
        dict_vacancies["city"] = get_in(item, ["area", "name"], "не указано")
        dict_vacancies["vacancy"] = item.get("name",
                                             "не указано")  # Используем .get() для прямого доступа к ключу верхнего уровня
        dict_vacancies["salary_from"] = get_in(item, ["salary", "from"], 0)
        dict_vacancies["salary_to"] = get_in(item, ["salary", "to"], 0)
        dict_vacancies["requirements"] = get_in(item, ["snippet", "responsibility"], "не указано")
        dict_vacancies["url"] = item.get("alternate_url",
                                         "не указано")  # Используем .get() для прямого доступа к ключу верхнего уровня
        list_vac.append(dict_vacancies)
        return list_vac
