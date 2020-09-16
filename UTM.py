import re
import datetime
from UTMExceptions import UTMNotConnect, DocumentNotFound
import requests
from lxml import objectify as ob


class UTM:

    def __init__(self, address, port):
        self.connector = 'http://' + address + ':' + str(port)
        self.fsrar = self._get_fsrar()
        try:
            requests.get(self.connector)
        except ConnectionError:
            raise UTMNotConnect('Could not connect to UTM')

    def _get_raw(self, url):
        return requests.get(self.connector + '/' + url).text

    def _get_fsrar(self):
        resp = self._get_raw('diagnosis')
        resp = resp.replace("""<?xml version="1.0" encoding="UTF-8" standalone="no"?>""", '')
        obj = ob.fromstring(resp)
        return obj.CN

    def _clean(self, raw):
        raw = raw.replace("""<?xml version="1.0" encoding="UTF-8" standalone="no"?>""", '')
        raw = raw.replace("""<?xml version="1.0" encoding="utf-8" standalone="no"?>""", '')
        raw = raw.replace("""<?xml version="1.0" encoding="utf-8"?>""", '')
        raw = raw.replace("""<?xml version="1.0" encoding="UTF-8"?>""", '')
        raw = re.sub(r'(?<=\w):(?=\w[^<>]*>)(?!\w+=)', '', raw)
        return raw


class UTMDocumentIN(UTM):
    URL = 'opt/out'

    def __init__(self, address, port):
        super().__init__(address, port)

    def _getType(self, doc):
        return re.split(r'/', doc.text)[-2]

    def getByReplyId(self, replyId):
        xml_raw = self._get_raw(self.URL)
        for doc in ob.fromstring(self._clean(xml_raw)).url:
            if doc.attrib.get('replyId') == replyId:
                self.url = doc.text
                self.replyId = doc.attrib.get('replyId', '00000000-0000-0000-0000-000000000000')
                self.type = self._getType(doc)
                return self
        raise DocumentNotFound()

    def getObjByReplyId(self, replyId):
        return UTMTicket(self.getByReplyId(replyId).url)


class UTMDocumentOUT(UTM):

    def __init__(self):
        super().__init__()


class UTMTicket(UTM):
    def __init__(self, url):
        ticket = ob.fromstring(self._get_raw(url))
        self.Date = datetime.datetime.strptime(ticket.nsDocument.nsTicket.tcTicketDate.text, '%Y-%m-%dT%H:%M:%S.%f')
        self.Identity = ticket.nsDocument.nsTicket.tcIdentity.text
        self.DocId = ticket.nsDocument.nsTicket.tcDocId.text
        self.TransportId = ticket.nsDocument.nsTicket.tcTransportId.text
        self.RegID = ticket.nsDocument.nsTicket.tcRegID.text
        self.DocType = ticket.nsDocument.nsTicket.tcDocType.text

    def _get_raw(self, url):
        try:
            raw = requests.get(url)
        except ConnectionError:
            raise UTMNotConnect('Could not connect to UTM')
        return self._clean(raw.text)
