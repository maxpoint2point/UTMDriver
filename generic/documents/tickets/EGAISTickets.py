from generic.documents.tickets.Ticket import Ticket
import datetime
from generic.queries.utm import requests


class EGAISTicket(Ticket):

    def __init__(self, connector, xml_data, doc_url):
        self.TicketDate = datetime.datetime.strptime(
            xml_data.nsDocument.nsTicket.tcTicketDate.text[:-1],
            '%Y-%m-%dT%H:%M:%S.%f'
        )
        self.Identity = xml_data.nsDocument.nsTicket.tcIdentity.text
        self.DocId = xml_data.nsDocument.nsTicket.tcDocId.text
        self.TransportId = xml_data.nsDocument.nsTicket.tcTransportId.text
        self.RegID = xml_data.nsDocument.nsTicket.tcRegID.text
        self.DocType = xml_data.nsDocument.nsTicket.tcDocType.text
        self.OperationName = xml_data.nsDocument.nsTicket.tcOperationResult.tcOperationName.text
        self.OperationResult = xml_data.nsDocument.nsTicket.tcOperationResult.tcOperationResult.text
        self.OperationDate = datetime.datetime.strptime(
            xml_data.nsDocument.nsTicket.tcOperationResult.tcOperationDate.text,
            '%Y-%m-%dT%H:%M:%S.%f'
        )
        self.OperationComment: str = xml_data.nsDocument.nsTicket.tcOperationResult.tcOperationComment.text
        self.connector = connector
        self.doc_url = doc_url

    def __str__(self):
        return f"{self.OperationResult}, {self.OperationDate}, ({self.TransportId})"

    def __bool__(self):
        if self.OperationResult == "Accepted":
            return True
        else:
            return False

    def delete(self):
        requests.delete(self.doc_url)
        return True
