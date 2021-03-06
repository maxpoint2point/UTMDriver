#  Copyright (c) maxpoint2point@gmail.com 2020.

from ....generic.documents.tickets.Ticket import Ticket
import datetime
from ....generic.queries.utm import requests


class UTMTicket(Ticket):

    def __init__(self, connector, xml_data, doc_url):
        self.TicketDate = datetime.datetime.strptime(
            xml_data.nsDocument.nsTicket.tcTicketDate.text[:-1],
            '%Y-%m-%dT%H:%M:%S.%f',
        )
        self.Identity = xml_data.nsDocument.nsTicket.tcIdentity.text
        self.DocId = xml_data.nsDocument.nsTicket.tcDocId.text
        self.TransportId = xml_data.nsDocument.nsTicket.tcTransportId.text
        self.RegID = xml_data.nsDocument.nsTicket.tcRegID.text
        self.DocType = xml_data.nsDocument.nsTicket.tcDocType.text
        self.Conclusion = xml_data.nsDocument.nsTicket.tcResult.tcConclusion.text
        self.ConclusionDate = datetime.datetime.strptime(
            xml_data.nsDocument.nsTicket.tcResult.tcConclusionDate.text[:-1],
            '%Y-%m-%dT%H:%M:%S.%f',
        )
        self.Comments = xml_data.nsDocument.nsTicket.tcResult.tcComments.text
        self.connector = connector
        self.doc_url = doc_url

    def __str__(self):
        return f"{self.Conclusion}, {self.ConclusionDate}, ({self.TransportId})"

    def __bool__(self):
        if self.Conclusion == "Accepted":
            return True
        else:
            return False

    def delete(self):
        requests.delete(self.doc_url)
        return True
