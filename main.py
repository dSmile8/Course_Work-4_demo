from src.hhru import WorkWithFile, HeadHunterAPI, VacanciesManager
from src.top import TopN


def user_interaction():
    search_query = input("Введите поисковый запрос: ")
    top_n = int(input("Введите количество вакансий для вывода в топ N: "))
    schedule = input("Введите ключевые слова для фильтрации вакансий по графику работы:\n"
                     "Например: Полный день / Вахта / Удаленная ").lower().split()
    work_with_file = WorkWithFile()
    top = TopN(top_n, schedule)
    vacancies = HeadHunterAPI().get_vacancies(search_query)
    work_with_file.save_to_json(vacancies)
    vacancies_manager = VacanciesManager()
    sorted_list = vacancies_manager.sorted_list()
    work_with_file.save_to_json(sorted_list)
    vacancies_manager.data_from_json()
    top.get_top_n()


if __name__ == "__main__":
    user_interaction()