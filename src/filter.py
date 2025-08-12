from pydoc import resolve
from typing import List

import f
from funcy import get_in


class Filter:
    """Класс для фильтрации данных с hh.ru"""

    def __init__(self, data):
        self.data = data

    @staticmethod
    def list_dict(item) -> List:
        """Метод для преобразования данных"""
        result = []
        for data in item:
            dict_vacancies = {"company": f.ichain(data, "employer", "name") or "не указана компания",
                              "city": f.ichain(data, "area", "name") or "не найдено",
                              "vacancy": data.get("name", "не указано"),
                              "salary_from": f.ichain(data, "salary", "from") or 0,
                              "salary_to": f.ichain(data, "salary", "to") or 0,
                              "requirements": f.ichain(data, "snippet", "responsibility") or "не указано",
                              "url": data.get("alternate_url",
                                              "не указано")}
            result.append(dict_vacancies)

        return result
