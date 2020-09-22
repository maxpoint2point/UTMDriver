from abc import ABC, abstractmethod


class NaTTN(ABC):
    def __init__(self, ):
        pass


class Ticket(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def delete(self):
        pass


class Position(ABC):
    def __init__(self):
        pass


class Rests(ABC):
    def __init__(self):
        pass
