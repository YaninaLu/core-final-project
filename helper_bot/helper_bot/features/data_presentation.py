from abc import abstractmethod, ABC


class DataPresenter(ABC):

    @staticmethod
    @abstractmethod
    def show_data(data):
        pass

class RecordsPresenter(DataPresenter):

    @staticmethod
    def show_data(data: dict) -> str:
        result = ""
        for record in data.values():
            result += "\n" + str(record) + "\n"
        return result
