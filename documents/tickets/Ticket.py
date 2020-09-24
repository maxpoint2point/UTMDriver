from abc import ABC, abstractmethod
import datetime


class Ticket(ABC):
    TicketDate: datetime = None
    Identity: str = ''
    DocId: str = ''
    TransportId: str = ''
    RegID: str = ''
    DocType: str = ''
    connector = None
    doc_url = None

    @abstractmethod
    def delete(self):
        pass

    @abstractmethod
    def __str__(self):
        pass

    @abstractmethod
    def __bool__(self):
        pass
