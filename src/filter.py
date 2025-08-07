from typing import List

import f


class Filter:
    """Класс для фильтрации данных с hh.ru"""

    def __init__(self, data):
        self.data = data

    def list_dict(self) -> List:
        """Метод для преобразование данных"""
        list_vac = []
        for i in self.data:
            dict_vacancies = {}
            dict_vacancies["company"] = f.ichain(i, "employer", "name") or "не указана компания"
            dict_vacancies["city"] = f.ichain(i, "area", "name") or "не указано"
            dict_vacancies["vacancy"] = f.ichain(i, "name") or "не указано"
            dict_vacancies["salary_from"] = f.ichain(i, "salary", "from") or 0
            dict_vacancies["salary_to"] = f.ichain(i, "salary", "to") or 0
            dict_vacancies["requirements"] = f.ichain(i, "snippet", "responsibility") or "не указано"
            dict_vacancies["url"] = f.ichain(i, "alternate_url") or "не указано"
            list_vac.append(dict_vacancies)
        return list_vac
