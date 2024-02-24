from src.hhru import WorkWithFile


class TopN(WorkWithFile):
    """Класс для финальной обработки данных, по запросам пользователя"""

    def __init__(self, n, schedule):
        super().__init__()
        self.n = n
        self.schedule = schedule

    @classmethod
    def sort_list_salary(cls, data_list):
        """Сортируем список словарей по ключу: средняя_зп"""

        return sorted(data_list, key=lambda k: k['average_salary'])[::-1]

    def get_sort_schedule(self):
        """Сортируем список по ключевым словам, входящим в рабочий график"""

        schedule_sort_list = []
        sorted_list = self.sort_list_salary(WorkWithFile.data_from_json(self))
        for i in sorted_list:
            for word in self.schedule:
                if i['schedule'].find(word) != -1:  # Если слово найдено
                    schedule_sort_list.append(i)    # Добавляем словарь в список schedule_sort_list
            if not self.schedule:  # если пользователь ничего не ввел, добавляем в список вакансии со всеми расписаниями
                schedule_sort_list.append(i)

        return schedule_sort_list

    def get_top_n(self):
        """Получаем список из N элементов и выводим словари этого списка"""

        for i in self.get_sort_schedule()[0:self.n]:
            print(i)
