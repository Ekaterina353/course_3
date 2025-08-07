from typing import List

import requests


class Parser:
    """Класс для подключения к api hh.ru"""

    def __init__(self):
        self.url = "https://api.hh.ru/vacancies"

    def connect(self) -> bool:
        """Метод проверки подключения"""
        responce = requests.get(self.url)
        return responce.status_code == 200

    def api(self, word: str) -> List:
        """Метод для получения списка вакансий(словарей)"""
        if self.connect():

            params = {"text": word, "per_page": 100, "area": "1859"}
            responce = requests.get(self.url, params)
            return responce.json()["items"]
        else:
            raise ValueError("Ошибка с интернетом")
