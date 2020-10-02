import datetime

from generic.positions import Position
from generic.textTransform import clean
from generic import UtmRequest


class ReplyNATTN:
    def __init__(self, connector, xml_data, doc_url):
        self.Position = []
        self.ReplyDate = datetime.datetime.strptime(
            xml_data.nsDocument.nsReplyNoAnswerTTN.ttnReplyDate.text,
            "%Y-%m-%dT%H:%M:%S.%f"
        )
        self.connector = connector
        self.doc_url = doc_url
        self.Consignee = xml_data.nsDocument.nsReplyNoAnswerTTN.ttnConsignee

        for ttn in xml_data.nsDocument.nsReplyNoAnswerTTN.ttnttnlist.ttnNoAnswer:
            self.Position.append(
                Position(
                    'ReplyNATTN',
                    WbRegID=ttn.ttnWbRegID,
                    ttnNumber=ttn.ttnttnNumber,
                    ttnDate=datetime.datetime.strptime(ttn.ttnttnDate.text, "%Y-%m-%d"),
                    Shipper=ttn.ttnShipper,
                )
            )

    def delete(self):
        UtmRequest.delete(self.doc_url)
        return True


class QueryNATTN:
    """
    Запрос списка не принятых накладных
    """
    def __init__(self, connector):
        from lxml import objectify as ob
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
