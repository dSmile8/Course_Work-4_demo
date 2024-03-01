from abc import ABC, abstractmethod

import json
from pathlib import Path


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
