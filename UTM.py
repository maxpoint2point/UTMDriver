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
        try:
            requests.get(self.base_url)
        except ConnectionError:
            raise UTMNotConnect('Could not connect to UTM')
        resp = self._get_raw('diagnosis')
        resp = resp.replace("""<?xml version="1.0" encoding="UTF-8" standalone="no"?>""", '')
        obj = ob.fromstring(resp)
        self.fsrar = obj.CN

    def _get_raw(self, url):
        return requests.get(self.base_url + '/' + url).text

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

    def deleteAll(self):
        docs = self.getAll()
        for doc in docs:
            try:
                requests.delete(doc.url)
            except ConnectionError:
                raise UTMNotConnect
        return True

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

    def getByType(self, doc_type):
        xml_raw = self._get_raw(self.URL_IN)
        obj = []
        for doc in ob.fromstring(_clean(xml_raw)).url:
            if _get_type(doc) == doc_type:
                obj.append(
                    UTMDocumentIN(
                        doc.text,
                        doc.attrib.get('replyId', '00000000-0000-0000-0000-000000000000'),
                        doc_type,
                    )
                )
        if not obj:
            raise EmptyResponse()
        return obj


class UTMDocumentIN:
    """
    Входящие документы в УТМ
    """

    def __init__(self, url, reply_id, doc_type):
        self.url = url
        self.reply_id = reply_id
        self.type = doc_type

    def __str__(self):
        return "{} {} {}".format(self.reply_id, self.type, self.url)

    def detail(self):
        if self.type == 'Ticket':
            return UTMTicket(self.url)

    def delete(self):
        try:
            requests.delete(self.url)
        except ConnectionError:
            raise UTMNotConnect
        return True


class UTMTicket:
    """
    Тикеты
    """

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

    def delete(self):
        try:
            requests.delete(self.url)
        except ConnectionError:
            raise UTMNotConnect()
        return True


class Position:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


class Rests:
    def __init__(self):
        pass


class ReplyRests(Rests):
    def __init__(self, url):
        super().__init__()
        self.url = url
        doc = ob.fromstring(_get_raw(url))
        self.date = datetime.datetime.strptime(doc.nsDocument.nsReplyRests.rstRestsDate.text, '%Y-%m-%dT%H:%M:%S.%f')
        self.position = []
        for line in doc.nsDocument.nsReplyRests.rstProducts.rstStockPosition:
            self.position.append(
                Position(
                    Quantity=line.rstQuantity.text,
                    InformARegId=line.rstInformARegId.text,
                    InformBRegId=line.rstInformBRegId.text,
                    FullName=line.rstProduct.prefFullName.text,
                    AlcCode=line.rstProduct.prefAlcCode.text,
                    Capacity=float(line.rstProduct.prefCapacity.text),
                    AlcVolume=float(line.rstProduct.prefAlcVolume.text),
                    VCode=line.rstProduct.prefProductVCode.text,
                    ProducerClientRegId=line.rstProduct.prefProducer.orefClientRegId.text,
                    ProducerINN=line.rstProduct.prefProducer.orefINN.text,
                    ProducerKPP=line.rstProduct.prefProducer.orefKPP.text,
                    ProducerFullName=line.rstProduct.prefProducer.orefFullName.text,
                    ProducerShortName=line.rstProduct.prefProducer.orefShortName.text,
                    addressCountry=line.rstProduct.prefProducer.orefaddress.orefCountry.text,
                    addressRegionCode=line.rstProduct.prefProducer.orefaddress.orefRegionCode.text,
                    addressdescription=line.rstProduct.prefProducer.orefaddress.orefdescription.text,
                )
            )

    def delete(self):
        try:
            requests.delete(self.url)
        except ConnectionError:
            raise UTMNotConnect
        return True


class QueryRests(Rests):
    def __init__(self):
        super().__init__()

    def send(self, **kwargs):
        pass


class NaTTNPosition:
    def __init__(self, **kwargs):
        self.WbRegID = kwargs['WbRegID']
        self.ttnNumber = kwargs['ttnNumber']
        self.Date = kwargs['Date']
        self.Shipper = kwargs['Shipper']

    def __str__(self):
        return "{} ({})".format(self.WbRegID, self.Date)


class NaTTN:
    def __init__(self, ):
        pass


class ReplyNaTTN(NaTTN):
    def __init__(self, url):
        super().__init__()
        self.url = url
        self.NoAnswerTTN = []
        doc = ob.fromstring(_get_raw(url))
        self.reply_date = datetime.datetime.strptime(
            doc.nsDocument.nsReplyNoAnswerTTN.ttnReplyDate.text,
            '%Y-%m-%dT%H:%M:%S.%f'
        )
        for nattn in doc.nsDocument.nsReplyNoAnswerTTN.ttnttnlist.ttnNoAnswer:
            self.NoAnswerTTN.append(
                NaTTNPosition(
                    WbRegID=nattn.ttnWbRegID.text,
                    ttnNumber=nattn.ttnttnNumber.text,
                    Date=datetime.datetime.strptime(nattn.ttnttnDate.text, '%Y-%m-%d'),
                    Shipper=nattn.ttnShipper.text,
                )
            )

    def delete(self):
        try:
            requests.delete(self.url)
        except ConnectionError:
            raise UTMNotConnect
