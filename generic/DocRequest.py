from generic import UtmRequest
from generic.textTransform import clean
from lxml import objectify as ob


class Request:
    replyId = None
    sign = None
    ok = None
    doc_type = None

    def __init__(self, connector, doc_type, **kwargs):
        self.doc_type = doc_type

        if self.doc_type == "NATTN":
            full_url = f"{connector.base_url}/opt/in/QueryNATTN"
            query = {
                'xml_file': (
                    'QueryNATTN.xml',
                    '<?xml version="1.0" encoding="UTF-8"?><ns:Documents Version="1.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:ns="http://fsrar.ru/WEGAIS/WB_DOC_SINGLE_01" xmlns:qp="http://fsrar.ru/WEGAIS/QueryParameters"><ns:Owner><ns:FSRAR_ID>' + connector.FSRAR + '</ns:FSRAR_ID></ns:Owner><ns:Document><ns:QueryNATTN><qp:Parameters><qp:Parameter><qp:Name>КОД</qp:Name><qp:Value>' + connector.FSRAR + '</qp:Value></qp:Parameter></qp:Parameters></ns:QueryNATTN></ns:Document></ns:Documents>',
                    'application/xml'
                )
            }
            r = UtmRequest.post(full_url, query)
            xml = ob.fromstring(clean(r))

            self.replyId = xml.url.text
            self.sign = xml.sign.text
            self.ok = r.ok

        if self.doc_type == "RestShop_v2":
            full_url = f"{connector.base_url}/opt/in/QueryRestsShop_v2"
            query = {
                'xml_file': (
                    'QueryRestsShop.xml',
                    '<?xml version="1.0" encoding="UTF-8"?><ns:Documents Version="1.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:ns="http://fsrar.ru/WEGAIS/WB_DOC_SINGLE_01" xmlns:qp="http://fsrar.ru/WEGAIS/QueryParameters"><ns:Owner><ns:FSRAR_ID>' + connector.FSRAR + '</ns:FSRAR_ID></ns:Owner><ns:Document><ns:QueryRestsShop_v2></ns:QueryRestsShop_v2></ns:Document></ns:Documents>',
                    'application/xml'
                )
            }
            r = UtmRequest.post(full_url, query)
            xml = ob.fromstring(clean(r))
            self.replyId = xml.url.text
            self.sign = xml.sign.text
            self.ok = r.ok

        if self.doc_type == "RestStore":
            full_url = f"{connector.base_url}/opt/in/QueryRests"
            query = {
                'xml_file': (
                    'QueryParameters.xls',
                    '<?xml version="1.0" encoding="UTF-8"?><ns:Documents Version="1.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:ns="http://fsrar.ru/WEGAIS/WB_DOC_SINGLE_01" xmlns:qp="http://fsrar.ru/WEGAIS/QueryParameters"><ns:Owner><ns:FSRAR_ID>' + connector.FSRAR + '</ns:FSRAR_ID></ns:Owner><ns:Document><ns:QueryRests></ns:QueryRests></ns:Document></ns:Documents>',
                    'application/xml'
                )
            }
            r = UtmRequest.post(full_url, query)
            xml = ob.fromstring(clean(r))
            self.replyId = xml.url.text
            self.sign = xml.sign.text
            self.ok = r.ok

        if self.doc_type == "TTN":
            full_url = f"{connector.base_url}/opt/in/QueryResendDoc"
            query = {
                'xml_file': (
                    'QueryParameters.xls',
                    '<?xml version="1.0" encoding="UTF-8"?><ns:Documents Version="1.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:ns="http://fsrar.ru/WEGAIS/WB_DOC_SINGLE_01" xmlns:qp="http://fsrar.ru/WEGAIS/QueryParameters"><ns:Owner><ns:FSRAR_ID>' + connector.FSRAR + '</ns:FSRAR_ID></ns:Owner><ns:Document><ns:QueryResendDoc><qp:Parameters><qp:Parameter><qp:Name>WBREGID</qp:Name><qp:Value>' + kwargs['TTN'] + '</qp:Value></qp:Parameter></qp:Parameters></ns:QueryResendDoc></ns:Document></ns:Documents>',
                    'application/xml'
                )
            }
            r = UtmRequest.post(full_url, query)
            xml = ob.fromstring(clean(r))
            self.replyId = xml.url.text
            self.sign = xml.sign.text
            self.ok = r.ok

    def __str__(self):
        return f"<{self.doc_type} [{self.ok}]>"
