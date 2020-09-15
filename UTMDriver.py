import requests
import re
from lxml import objectify as ob
from UTMExceptions import *

class UTMDriver():
    """Обеспечение свзяи между утм и приложениями"""
    address = None
    port = None
    _url_in = None
    _url_out = None

    def __init__(self, address, port):
        port = str(port)
        self._url_in = 'http://'+address+':'+port+'/opt/in'
        self._url_out = 'http://'+address+':'+port+'/opt/out'

        try:
            requests.get('http://'+address+':'+port)
        except ConnectionError:
            raise UTMNotConnect

    def _getData(self, response):
        """Очистка xml ответа от лишнего мусора"""
        response = response.replace("""<?xml version="1.0" encoding="UTF-8" standalone="no"?>""", '')
        response = response.replace("""<?xml version="1.0" encoding="utf-8" standalone="no"?>""", '')
        response = response.replace("""<?xml version="1.0" encoding="utf-8"?>""", '')
        response = response.replace("""<?xml version="1.0" encoding="UTF-8"?>""", '')
        response = re.sub(r'(?<=\w):(?=\w[^<>]*>)(?!\w+=)', '', response)
        return ob.fromstring(response)

    def _connect(self, d = None):
        if not d == None:
            r = requests.get(self._url_in)
        else:
            r = requests.get(self._url_out)
        return self._getData(r.text)

    def deleteDocument(self, url):
        try:
            requests.delete(url)
        except ConnectionError:
            return False
        else:
            return True

    def _getType(self, doc):
        return re.split(r'/', doc.text)[-2]

    def getOutDocuments(self):
        """Получить список исходящих документов и вернуть объект или исключение EmptyResponse"""
        xml = self._connect(True)
        if not hasattr(xml, 'url'):
            raise EmptyResponce("Empty")
        return xml

    def getInDocuments(self):
        """Получить список входящих документов и вернуть список кортежей или исключение EmptyResponse"""
        xml = self._connect()
        docs = []
        if not hasattr(xml, 'url'):
            raise EmptyResponse("Empty")
        for doc in xml.url:
            #если нет replyId = 00000000-0000-0000-0000-000000000000
            docs.append((self._getType(doc), doc.attrib['replyId'], doc))
        return docs

    def getInDocumentUrlByReplyId(self, replyId):
        """Получить входящий документ по replyId или вернуть исключение DocumentNotFound"""
        xml = self._connect()
        if not hasattr(xml, 'url'):
            raise EmptyResponse("Empty")
        for doc in xml.url:
            if doc.attrib['replyId'] == replyId:
                type = self._getType(doc)
                return type, doc
        raise DocumentNotFound("Document with replyId not Found")

    def getDocumentsByType(self, type):
        docs = []
        xml = self._connect()
        if not hasattr(xml, 'url'):
            raise EmptyResponse("Empty")
        for doc in xml.url:
            if self._getType(doc) == type:
                docs.append(doc)
        return docs
