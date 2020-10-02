from documents.rests.rest import *
from generic.positions import Position
import datetime
from generic import UtmRequest
from generic.textTransform import clean


class StoreRest(Rest):
    def __init__(self, connector, xml_data, doc_url):
        self.RestDate = datetime.datetime.strptime(
            xml_data.nsDocument.nsReplyRests.rstRestsDate.text,
            "%Y-%m-%dT%H:%M:%S.%f"
        )
        for good in xml_data.nsDocument.nsReplyRests.rstProducts.rstStockPosition:
            self.Position.append(
                Position(
                    'StoreRest',
                    StockPositionQuantity=good.rstQuantity.text,
                    StockPositionInformARegId=good.rstInformARegId.text,
                    StockPositionInformBRegId=good.rstInformBRegId.text,
                    ProductFullName=good.rstProduct.prefFullName.text,
                    ProductAlcCode=good.rstProduct.prefAlcCode.text,
                    ProductCapacity=good.rstProduct.prefCapacity.text,
                    ProductAlcVolume=good.rstProduct.prefAlcVolume.text,
                    ProductVCode=good.rstProduct.prefProductVCode.text,
                    ProducerClientRegId=good.rstProduct.prefProducer.orefClientRegId.text,
                    ProducerINN=good.rstProduct.prefProducer.orefINN.text,
                    ProducerKPP=good.rstProduct.prefProducer.orefKPP.text,
                    ProducerFullName=good.rstProduct.prefProducer.orefFullName.text,
                    ProducerShortName=good.rstProduct.prefProducer.orefShortName.text,
                    addressCountry=good.rstProduct.prefProducer.orefaddress.orefCountry.text,
                    addressRegionCode=good.rstProduct.prefProducer.orefaddress.orefRegionCode.text,
                    addressDescription=good.rstProduct.prefProducer.orefaddress.orefdescription.text,
                )
            )
        self.connector = connector
        self.doc_url = doc_url

    def delete(self):
        UtmRequest.delete(self.doc_url)
        return True

    def push(self):
        pass

    def __str__(self):
        return f"{self.RestDate}, {self.doc_url}"


class QueryStoreRests:
    def __init__(self, connector):
        from lxml import objectify as ob
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
