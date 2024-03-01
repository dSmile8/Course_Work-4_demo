from src.work_with_file import WorkWithFile


class VacanciesManager:
    all = []

    def __init__(self, name=None, url=None, salary=0, salary_from=None, salary_to=None, currency=None, schedule=None,
                 average_salary=None, area=None):
        self.vacancies_list = None
        a = WorkWithFile()
        self.data = a.data_from_json()['items']
        self.name = name
        self.url = url
        self.salary = salary
        self.salary_from = salary_from
        self.salary_to = salary_to
        self.currency = currency
        self.schedule = schedule
        self.average_salary = average_salary
        self.area = area


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
                'area': data['area']['name']
            }

            self.vacancies_list.append(vacancies_dict)
        self.get_average_salary()
        self.convert_currency()
        return self.vacancies_list

    def cast_to_object_list(cls, data) -> list:
        """
        Создает список объектов класса Vacancy по данным из sorted list
        """

        for item in data:
            name = item['name']
            url = item['url']
            salary = item['salary']
            salary_from = item['salary_from']
            salary_to = item['salary_to']
            currency = item['currency']
            schedule = item['schedule']
            average_salary = item['average_salary']
            area = item['area']

            vacancy = VacanciesManager(name, url, salary, salary_from, salary_to, currency, schedule, average_salary, area)
            VacanciesManager.all.append(vacancy)
        return VacanciesManager.all

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


    def __repr__(self):
        """Отображает информацию для разработчика"""
        return f'{self.__class__.__name__},{self.name}, {self.url}, {self.area}, {self.salary}, {self.salary_from}, ' \
               f'{self.salary_to}, {self.average_salary}, {self.currency}, {self.schedule}'


    def __str__(self) -> str:
        """
        Отображает информацию о ваканси для пользователей
        """
        return f'{self.name}: {self.salary}'

    def __ge__(self, other) -> bool:
        """
        Проверяет, является ли зарпата по данной вакансии выше или равна другой
        """
        if isinstance(other, self.__class__):
            return {self.average_salary} >= other.average_salary
        elif isinstance(other, int):
            return self.average_salary >= other
        else:
            raise TypeError("Сравнение данных объектов невозможно")

    def __gt__(self, other) -> bool:
        """
        Проверяет, является ли средняя зарпата по данной вакансии выше другой
        """
        if isinstance(other, self.__class__):
            return self.average_salary > other.average_salary
        elif isinstance(other, int):
            return self.average_salary > other
        else:
            raise TypeError("Сравнение данных объектов невозможно")

    def __le__(self, other) -> bool:
        """
        Проверяет, является ли зарпата по данной вакансии ниже или равна другой
        """
        if isinstance(other, self.__class__):
            return self.average_salary <= other.average_salary
        elif isinstance(other, int):
            return self.average_salary <= other
        else:
            raise TypeError("Сравнение данных объектов невозможно")

    def __lt__(self, other) -> bool:
        """
        Проверяет, является ли зарпата по данной вакансии ниже другой
        """
        if isinstance(other, self.__class__):
            return self.average_salary < other.average_salary
        elif isinstance(other, int):
            return self.average_salary < other
        else:
            raise TypeError("Сравнение данных объектов невозможно")