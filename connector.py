#  Copyright (c) maxpoint2point@gmail.com 2020.

from generic.exceptions import EmptyResponse
from generic.helpers.textTransform import getType, clean, unescape
from generic.queries.utm import requests
from generic.documents import certificate
from generic.queries.documents import DocRequest


class Connector:
    def __init__(self, address, port):
        requests.get(f"http://{address}:{str(port)}/")
        self.__response = requests.get(f"http://{address}:{str(port)}/diagnosis")
        self.base_url = f"http://{address}:{str(port)}"
        self.FSRAR = self.__getFSRAR(f"http://{address}:{str(port)}/diagnosis")
        self.status = self.__response.status_code

    def __str__(self):
        return f"UTM: {self.FSRAR} ({self.base_url}) status: {self.status}"

    def __getFSRAR(self, url):
        xml = self.__getXmlData(url)
        return xml.CN.text

    @staticmethod
    def __getXmlData(full_url):
        from lxml import objectify as ob
        raw = requests.get(full_url)
        raw = clean(raw)
        xml = ob.fromstring(raw)
        return xml

    def __returnObj(self, xml_data, doc_type, full_url):
        # TODO: Реализовать нормальный выбор типа документа
        if doc_type == 'Ticket':
            if hasattr(xml_data.nsDocument.nsTicket, 'tcOperationResult'):
                from generic.documents.tickets import EGAISTickets
                return EGAISTickets.EGAISTicket(self, xml_data, full_url)
            else:
                from generic.documents.tickets import UTMTickets
                return UTMTickets.UTMTicket(self, xml_data, full_url)
        if doc_type == 'ReplyRests':
            from generic.documents.rests import storeRest
            return storeRest.StoreRest(self, xml_data, full_url)
        if doc_type == 'ReplyRestsShop_v2':
            from generic.documents.rests import shopRest
            return shopRest.ShopRest(self, xml_data, full_url)
        if doc_type == 'ReplyNATTN':
            from generic.documents.NATTN import NATTN
            return NATTN.ReplyNATTN(self, xml_data, full_url)
        if doc_type == 'WayBill_v3':
            from generic.documents.waybill import waybill_v3
            return waybill_v3.WayBill_v3(self, xml_data, full_url)
        if doc_type == 'TTNHISTORYF2REG':
            from generic.documents.waybill import ttnHistoryF2Reg
            return ttnHistoryF2Reg.TTNHistoryF2Reg(self, xml_data, full_url)
        if doc_type == 'FORM2REGINFO':
            from generic.documents.waybill import form2reginfo
            return form2reginfo.Form2RegInfo(self, xml_data, full_url)

    def getByUrl(self, url):
        if url[0:7] == "http://":
            full_url = url
        else:
            full_url = f"{self.base_url}/opt/out/{url}"
        xml_data = self.__getXmlData(full_url)
        doc_type = getType(full_url)
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
                self.__returnObj(d, getType(doc.text), doc)
            )
        return obj

    def getByType(self, doc_type):
        full_url = f"{self.base_url}/opt/out/{doc_type}"
        xml_data = self.__getXmlData(full_url)
        if not hasattr(xml_data, 'url'):
            raise EmptyResponse
        obj = []
        for doc in xml_data.url:
            d = self.__getXmlData(doc)
            obj.append(
                self.__returnObj(d, doc_type, doc)
            )
        return obj

    def getAll(self):
        full_url = f"{self.base_url}/opt/out"
        xml_data = self.__getXmlData(full_url)
        if not hasattr(xml_data, 'url'):
            raise EmptyResponse
        obj = []
        for doc in xml_data.url:
            d = self.__getXmlData(doc)
            obj.append(
                self.__returnObj(d, getType(doc.text), doc)
            )
        return obj

    @property
    def total(self):
        full_url = f"{self.base_url}/opt/out/total"
        xml_data = self.__getXmlData(full_url)
        return int(xml_data.total.text)

    @property
    def version(self):
        full_url = f"{self.base_url}/info/version"
        v = requests.get(full_url)
        return v.text

    @property
    def dbtime(self):
        import datetime
        full_url = f"{self.base_url}/info/dbtime"
        d = datetime.datetime.strptime(
            requests.get(full_url).text,
            "%Y-%m-%d %H:%M:%S.%f"
        )
        return d

    @property
    def gost_cert(self):
        try:
            full_url = f"{self.base_url}/info/certificate/GOST"
            r = requests.get(full_url)
            r = unescape(r.text)
            cert = []
            for line in r.split('\n'):
                if 'Subject:' in line:
                    string = line[11:].split(", ")
                    for s in string:
                        cert.append(s.split("=")[1])
                if 'Validity:' in line:
                    cert.append(line[19:-1])
                if 'To:' in line:
                    cert.append(line[19:-1])
            return certificate.Certificate(
                cert='GOST',
                cn=cert[0],
                surname=cert[1],
                givenname=cert[2],
                c=cert[3],
                st=cert[4],
                l=cert[5],
                street=cert[6],
                emailaddress=cert[9],
                valid_from=cert[11],
                valid_to=cert[12]
            )
        except (IndexError, ValueError):
            return None

    @property
    def rsa_cert(self):
        full_url = f"{self.base_url}/info/certificate/RSA"
        r = requests.get(full_url)
        r = unescape(r.text)
        cert = []
        for line in r.split('\n'):
            if 'Subject:' in line:
                string = line[11:].split(", ")
                for s in string:
                    cert.append(s.split("=")[1])
            if 'Validity:' in line:
                cert.append(line[19:-1])
            if 'To:' in line:
                cert.append(line[19:-1])
        return certificate.Certificate(
            cert='RSA',
            cn=cert[1],
            valid_from=cert[7],
            valid_to=cert[8]
        )

    def request_document(self, doc_type, **kwargs):
        return DocRequest.Request(self, doc_type, **kwargs)

    def clearUTM(self):
        for document in self.getAll():
            requests.delete(document.doc_url)
        return True
