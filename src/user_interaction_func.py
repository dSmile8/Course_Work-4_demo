from src.hhru import VacanciesManager
from src.ApiVacancies import HeadHunterAPI
from src.top import sort_list_salary, get_vacancies_by_salary, get_top_n, get_sort_schedule, print_vacancies, \
    string_to_number
from src.work_with_file import WorkWithFile


def user_interaction():
    search_query = input("Введите поисковый запрос: ")
    desired_salary = input("Введите желаемую среднюю зарплату: ")
    desired_salary_int = string_to_number(desired_salary)  # преобразуем строку в число
    top_n = input("Введите количество вакансий для вывода в топ N: ")
    top_n_int = string_to_number(top_n)  # преобразуем строку в число
    schedule = input("Введите ключевые слова для фильтрации вакансий по графику работы:\n"
                     "Например: Полный день / Вахта / Удаленная \n").lower().split()
    work_with_file = WorkWithFile()
    vacancies = HeadHunterAPI(search_query).get_vacancies()
    work_with_file.save_to_json(vacancies)
    vacancies_manager = VacanciesManager()
    sorted_list = vacancies_manager.sorted_list()
    object_list = vacancies_manager.cast_to_object_list(sorted_list)  # получаем список объектов класса VacanciesManager
    sort_desired_salary = get_vacancies_by_salary(object_list, desired_salary_int)  # сортируем список по желаемой ЗП
    sort_list_by_average_salary = sort_list_salary(sort_desired_salary)  # сортируем список по средней ЗП
    sort_schedule = get_sort_schedule(sort_list_by_average_salary, schedule)  # сортируем список по желаемому графику
    top_list = get_top_n(sort_schedule, top_n_int)  # получаем желаемое количество вакансий в топ
    print_vacancies(top_list)  # печатаем информацию для пользователя
