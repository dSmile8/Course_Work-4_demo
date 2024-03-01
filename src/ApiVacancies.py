from abc import ABC, abstractmethod
import requests


class ApiVacancyService(ABC):

    @abstractmethod
    def get_vacancies(self):
        pass

    @abstractmethod
    def connecting_to_api(self):
        pass


class HeadHunterAPI(ApiVacancyService):
    def __init__(self, name):
        self.__url = 'https://api.hh.ru/vacancies'
        self.__name = name
        self.__params = {
            'text': self.__name,
            'per_page': 100,  # количество вакансий
            'area': '113'  # Регион. Необходимо передавать id из справочника /areas.
        }

    def connecting_to_api(self):
        """Подключаемся к апи HH.ru"""
        return requests.get(self.__url, params=self.__params)

    def get_vacancies(self):
        """
        Метод получает список вакансий
        """
        return self.connecting_to_api().json()

    @property
    def url(self):
        return self.__url

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, new_name):
        self.__name = new_name

