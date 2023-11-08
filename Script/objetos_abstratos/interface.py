import abc

class Interface(abc.ABC):
    def __init__(self, map_list, rect=0) -> None:
        self.map = map_list
        self.rect = rect
        self.estado = False

    @abc.abstractmethod
    def run(self):
        pass

    