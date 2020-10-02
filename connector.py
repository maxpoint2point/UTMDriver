from generic.exceptions import *
from lxml import objectify as ob
from documents.tickets import EGAISTickets, UTMTickets
from documents.rests import storeRest, shopRest
from documents.NATTN import NATTN

import requests
import re


class Connector:
    def __init__(self, address, port):
        try:
            self.__response = requests.get(f"http://{address}:{str(port)}/diagnosis")
            if self.__response.status_code != 200:
                raise UTMNotConnect
        except ConnectionError:
            raise UTMNotConnect
        self.base_url = f"http://{address}:{str(port)}"
        self.FSRAR = self.__getFSRAR(f"http://{address}:{str(port)}/diagnosis")
        self.status = self.__response.status_code

    def __str__(self):
        return f"UTM: {self.FSRAR} ({self.base_url}) status: {self.status}"

    def __getFSRAR(self, url):
        xml = self.__getXmlData(url)
        return xml.CN.text

    @staticmethod
    def __getType(full_url):
        return re.split(r'/', full_url)[-2]

    @staticmethod
    def __getXmlData(full_url):
        try:
            raw = requests.get(full_url)
            if raw.status_code == 404:
                raise DocumentNotFound
            if raw.status_code != 200:
                raise UTMNotConnect
        except requests.exceptions.ConnectionError:
            raise UTMNotConnect
        raw = raw.text.replace("""<?xml version="1.0" encoding="UTF-8" standalone="no"?>""", '')
        raw = raw.replace("""<?xml version="1.0" encoding="utf-8" standalone="no"?>""", '')
        raw = raw.replace("""<?xml version="1.0" encoding="utf-8"?>""", '')
        raw = raw.replace("""<?xml version="1.0" encoding="UTF-8"?>""", '')
        raw = re.sub(r'(?<=\w):(?=\w[^<>]*>)(?!\w+=)', '', raw)
        xml = ob.fromstring(raw)
        return xml

    def __returnObj(self, xml_data, doc_type, full_url):
        # TODO: Реализовать нормальный выбор типа документа
        if doc_type == 'Ticket':
            if hasattr(xml_data.nsDocument.nsTicket, 'tcOperationResult'):
                return EGAISTickets.EGAISTicket(self, xml_data, full_url)
            else:
                return UTMTickets.UTMTicket(self, xml_data, full_url)
        if doc_type == 'ReplyRests':
            return storeRest.StoreRest(self, xml_data, full_url)
        if doc_type == 'ReplyRestsShop_v2':
            return shopRest.ShopRest(self, xml_data, full_url)
        if doc_type == 'ReplyNATTN':
            return NATTN.ReplyNATTN(self, xml_data, full_url)

    def getInByUrl(self, url):
        if url[0:7] == "http://":
            full_url = url
        else:
            full_url = f"{self.base_url}/opt/out/{url}"
        xml_data = self.__getXmlData(full_url)
        doc_type = self.__getType(full_url)
        return self.__returnObj(xml_data, doc_type, full_url)

    def getByReplyId(self, replyId):
        full_url = f"{self.base_url}/opt/out?replyId={replyId}"
        xml_data = self.__getXmlData(full_url)
        if not hasattr(xml_data, 'url'):
            raise EmptyResponse
        obj = []
        for doc in xml_data.url:
            d = self.__getXmlData(doc)
            obj.append(
                self.__returnObj(d, self.__getType(doc.text), doc)
            )
        return obj

    def getByDocumentType(self, doc_type):
        full_url = f"{self.base_url}/opt/out/{doc_type}"
        xml_data = self.__getXmlData(full_url)
        obj = []
        for doc in xml_data.url:
            d = self.__getXmlData(doc)
            obj.append(
                self.__returnObj(d, doc_type, doc)
            )
        return obj
