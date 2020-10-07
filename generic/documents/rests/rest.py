from abc import ABC, abstractmethod


class Rest(ABC):
    RestDate = None
    connector = None
    doc_url = None
    Position = []

    @abstractmethod
    def push(self):
        pass

    @abstractmethod
    def delete(self):
        pass

    @abstractmethod
    def __str__(self):
        pass
