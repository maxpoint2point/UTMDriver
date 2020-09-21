import datetime
import re
import requests

from lxml import objectify as ob

from UTMExceptions import UTMNotConnect, DocumentNotFound, EmptyResponse


def _get_type(doc):
    return re.split(r'/', doc.text)[-2]


def _clean(raw):
    raw = raw.replace("""<?xml version="1.0" encoding="UTF-8" standalone="no"?>""", '')
    raw = raw.replace("""<?xml version="1.0" encoding="utf-8" standalone="no"?>""", '')
    raw = raw.replace("""<?xml version="1.0" encoding="utf-8"?>""", '')
    raw = raw.replace("""<?xml version="1.0" encoding="UTF-8"?>""", '')
    raw = re.sub(r'(?<=\w):(?=\w[^<>]*>)(?!\w+=)', '', raw)
    return raw


def _get_raw(url):
    try:
        raw = requests.get(url)
    except ConnectionError:
        raise UTMNotConnect('Could not connect to UTM')
    return _clean(raw.text)


def _getTicketType(ticket):
    if hasattr(ticket.nsDocument.nsTicket, 'tcResult'):
        return 'UTM'
    else:
        return 'EGAIS'


class UTM:
    URL_IN = 'opt/out'
    URL_OUT = 'opt/in'

    def __init__(self, address, port):
        self.base_url = 'http://' + address + ':' + str(port)
        self.fsrar = self._get_fsrar()
        try:
            requests.get(self.base_url)
        except ConnectionError:
            raise UTMNotConnect('Could not connect to UTM')

    def _get_raw(self, url):
        return requests.get(self.base_url + '/' + url).text

    def _get_fsrar(self):
        resp = self._get_raw('diagnosis')
        resp = resp.replace("""<?xml version="1.0" encoding="UTF-8" standalone="no"?>""", '')
        obj = ob.fromstring(resp)
        return obj.CN

    def getAll(self):
        xml_raw = self._get_raw(self.URL_IN)
        obj = []
        for doc in ob.fromstring(_clean(xml_raw)).url:
            obj.append(
                UTMDocumentIN(
                    doc.text,
                    doc.attrib.get('replyId', '00000000-0000-0000-0000-000000000000'),
                    _get_type(doc),
                )
            )
        if not obj:
            raise EmptyResponse
        return obj

    def getByReplyId(self, replyId):
        xml_raw = self._get_raw(self.URL_IN)
        obj = []
        for doc in ob.fromstring(_clean(xml_raw)).url:
            if doc.attrib.get('replyId') == replyId:
                obj.append(
                    UTMDocumentIN(
                        doc.text,
                        doc.attrib.get('replyId', '00000000-0000-0000-0000-000000000000'),
                        _get_type(doc),
                    )
                )
        if not obj:
            raise DocumentNotFound()
        return obj

    """def getDocumentByReplyId(self, reply_id):
        docs = self.getByReplyId(reply_id)
        obj = []
        for doc in docs:
            obj.append(
                UTMTicket(
                    doc.url
                )
            )
        return obj"""

    def getTickets(self):
        xml_raw = self._get_raw(self.URL_IN)
        obj = []
        for doc in ob.fromstring(_clean(xml_raw)).url:
            if _get_type(doc) == 'Ticket':
                obj.append(UTMTicket(doc))
        if not obj:
            raise EmptyResponse()
        return obj


class UTMDocumentIN:

    def __init__(self, url, reply_id, doc_type):
        self.url = url
        self.reply_id = reply_id
        self.type = doc_type

    def __str__(self):
        return "{} {} {}".format(self.reply_id, self.type, self.url)


class UTMTicket:
    def __init__(self, url):
        ticket = ob.fromstring(_get_raw(url))
        date_str = ticket.nsDocument.nsTicket.tcTicketDate.text
        if len(date_str) > 26:
            date_str = date_str[:-1]
        self.url = url
        self.Date = datetime.datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S.%f')
        self.Identity = ticket.nsDocument.nsTicket.tcIdentity.text
        self.DocId = ticket.nsDocument.nsTicket.tcDocId.text
        self.TransportId = ticket.nsDocument.nsTicket.tcTransportId.text
        self.RegID = ticket.nsDocument.nsTicket.tcRegID.text
        self.DocType = ticket.nsDocument.nsTicket.tcDocType.text

        self.ticket_type = _getTicketType(ticket)

        if self.ticket_type == 'UTM':
            if ticket.nsDocument.nsTicket.tcResult.tcConclusion == 'Accepted':
                self.result = True
            else:
                self.result = False
            date_str = ticket.nsDocument.nsTicket.tcResult.tcConclusionDate.text
            if len(date_str) > 26:
                date_str = date_str[:-1]
            self.result_date = datetime.datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S.%f')
            self.comment = ticket.nsDocument.nsTicket.tcResult.tcComments

        if self.ticket_type == 'EGAIS':
            if ticket.nsDocument.nsTicket.tcOperationResult.tcOperationResult == 'Accepted':
                self.result = True
            else:
                self.result = False
            self.result_date = datetime.datetime.strptime(
                ticket.nsDocument.nsTicket.tcOperationResult.tcOperationDate.text,
                '%Y-%m-%dT%H:%M:%S.%f')
            self.comment = ticket.nsDocument.nsTicket.tcOperationResult.tcOperationComment

    def __str__(self):
        return "Квитанция {}, Результат: {} {} ({})".format(
            self.ticket_type,
            self.result,
            self.comment,
            self.TransportId,
        )

    def __bool__(self):
        return self.result

    def UTMDelete(self):
        try:
            requests.delete(self.url)
            return True
        except ConnectionError:
            raise UTMNotConnect()
