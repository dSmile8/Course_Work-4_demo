def sort_list_salary(data_list) -> list:
    """Сортируем список вакансий по ключу: средняя_зп в порядке убывания"""
    return sorted(data_list, reverse=True)


def get_vacancies_by_salary(data_list, salary) -> list:
    """Отбирает вакансии по указанной средней зарплате (больше или равно указанной)"""
    if not isinstance(salary, int):
        salary = 0
    new_list = []
    for data in data_list:
        if data.average_salary >= salary:
            new_list.append(data)
    return new_list


def get_top_n(data_list, top_n):
    """Получаем список из N элементов и выводим словари этого списка"""
    if top_n == 0:
        return data_list
    else:
        return data_list[0:top_n]


def get_sort_schedule(data_list, schedule):
    """Сортируем список по ключевым словам, входящим в рабочий график"""

    schedule_sort_list = []
    for i in data_list:
        for word in schedule:
            if i.schedule.find(word) != -1:  # Если слово найдено
                schedule_sort_list.append(i)  # Добавляем словарь в список schedule_sort_list
        if not schedule:  # если пользователь ничего не ввел, добавляем в список вакансии со всеми расписаниями
            schedule_sort_list.append(i)
    return schedule_sort_list


def print_vacancies(data_list) -> None:
    """Печатаем информацию о вакансиях"""

    count = 0
    for data in data_list:
        print(f'{count + 1}) Вакансия: {data.name} / Ссылка: {data.url}\n'
              f'Город: {data.area}\n'
              f'Зарплата: {data.salary} {data.currency} / Средняя ЗП: {data.average_salary} {data.currency}\n'
              f'График работы: {data.schedule}\n'
              f'Требования: {data.requirement}\n')
        count += 1


def string_to_number(string) -> int:
    """
    Возвращает число из числа-строки
    :param string: строка
    :return: число
    """
    try:
        number = int(float(string))
        return number
    except ValueError:
        return 0
