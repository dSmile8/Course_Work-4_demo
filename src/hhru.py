from abc import ABC, abstractmethod
import requests
import json
from pathlib import Path


class ApiVacanciService(ABC):
    pass

    @abstractmethod
    def get_vacancies(self, name):
        pass


class HeadHunterAPI(ApiVacanciService):
    def __init__(self):
        self.url = 'https://api.hh.ru/vacancies'

    def get_vacancies(self, name: str = None):
        """
        Метод получает список вакансий
        :param name: название профессии
        """
        params = {
            'text': name,
            'per_page': 100,  # количество вакансий
            'area': '1'  # Регион. Необходимо передавать id из справочника /areas.
        }
        response = requests.get(self.url, params=params)
        vacancies = response.json()
        return vacancies


class BaseWorkWithFile(ABC):
    @abstractmethod
    def save_to_json(self, data):
        pass

    @abstractmethod
    def data_from_json(self):
        pass

    @abstractmethod
    def delete_data_from_json(self):
        pass


class WorkWithFile(BaseWorkWithFile):
    DATA_DIR = Path(__file__).parent.parent.joinpath('data', 'hh.json')

    def __init__(self):
        self.data = None

    def save_to_json(self, data1):
        """Сохраняет данные в файл"""

        self.data = data1
        with open(self.DATA_DIR, "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False)

    def data_from_json(self):
        """Получает данные из файла"""

        with open(WorkWithFile.DATA_DIR, "r", encoding="utf-8") as f:
            data_dict = json.load(f)
            return data_dict

    def delete_data_from_json(self):
        pass


class VacanciesManager(WorkWithFile):
    def __init__(self):
        super().__init__()
        self.vacancies_list = None
        self.data = WorkWithFile.data_from_json(self)['items']

    def sorted_list(self):
        """Сортирует JSON файл и возвращает новый список словарей с нужными нам параметрами """

        self.vacancies_list = []
        for data in self.data:
            salary_from = 0
            salary_to = 0
            currency = ''

            if data['salary'] is None:
                salary = 'ЗП не указана'
            else:
                if data['salary']['from'] is not None:
                    salary_from = data['salary']['from']
                    currency = data['salary']['currency']
                if data['salary']['to'] is not None:
                    salary_to = data['salary']['to']
                    currency = data['salary']['currency']
                salary = f"{salary_from} - {salary_to}"

            vacancies_dict = {
                'name': data['name'],
                'url': data['alternate_url'],
                'salary': salary,
                'salary_from': salary_from,
                'salary_to': salary_to,
                'currency': currency,
                'schedule': data['schedule']['name'].lower(),
            }

            self.vacancies_list.append(vacancies_dict)
        self.get_average_salary()
        self.convert_currency()
        return self.vacancies_list

    def get_average_salary(self):
        """Получаем значение средней зарплаты и добавляем в список новый ключ: average_salary
           Средняя зарплата считается следующим образом:
           Если ЗП указана 'до N', то берется среднее между 0 и N
           Если ЗП указана 'от N', без указания верхней границы, то берется значение 'от N'
           Если ЗП указана 'от N до M', то берется среднее между N и M
           """

        for data in self.vacancies_list:
            if data['salary_from'] == 0 and data['salary_to'] == 0:
                data["average_salary"] = 0
            if data['salary_from'] == 0 and data['salary_to'] != 0:
                data["average_salary"] = data['salary_to'] / 2
            if data['salary_from'] != 0 and data['salary_to'] == 0:
                data["average_salary"] = data['salary_from']
            if data['salary_from'] != 0 and data['salary_to'] != 0:
                data["average_salary"] = (data['salary_from'] + data['salary_to']) / 2

    def convert_currency(self):
        """Конвертируем USD в RUR"""

        for data in self.vacancies_list:
            if data['currency'] == 'USD':
                data['salary_from'] *= 100
                data['salary_to'] *= 100
                data['salary'] = f"{data['salary_from']} - {data['salary_to']}"
                data['currency'] = 'RUR'

