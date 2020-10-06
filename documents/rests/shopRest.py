from documents.rests.rest import *
from generic.positions import Position
import datetime
from generic import UtmRequest


class ShopRest(Rest):
    def __init__(self, connector, xml_data, doc_url):
        self.RestDate = datetime.datetime.strptime(
            xml_data.nsDocument.nsReplyRestsShop_v2.rstRestsDate.text,
            "%Y-%m-%dT%H:%M:%S"
        )
        for good in xml_data.nsDocument.nsReplyRestsShop_v2.rstProducts.rstShopPosition:
            self.Position.append(
                Position(
                    'ShopRests_v2',
                    ShopPositionQuantity=good.rstQuantity,
                    ProductFullName=good.rstProduct.prefFullName,
                    ProductAlcCode=good.rstProduct.prefAlcCode,
                    ProductCapacity=good.rstProduct.prefCapacity,
                    ProductUnitType=good.rstProduct.prefUnitType,
                    ProductAlcVolume=good.rstProduct.prefAlcVolume,
                    ProductVCode=good.rstProduct.prefProductVCode,
                    ProducerClientRegId=good.rstProduct.prefProducer.orefUL.orefClientRegId,
                    ProducerINN=good.rstProduct.prefProducer.orefUL.orefINN,
                    ProducerKPP=good.rstProduct.prefProducer.orefUL.orefKPP,
                    ProducerFullName=good.rstProduct.prefProducer.orefUL.orefFullName,
                    ProducerShortName=good.rstProduct.prefProducer.orefUL.orefShortName,
                    addressCountry=good.rstProduct.prefProducer.orefUL.orefaddress.orefCountry,
                    addressRegionCode=good.rstProduct.prefProducer.orefUL.orefaddress.orefRegionCode,
                    addressdescription=good.rstProduct.prefProducer.orefUL.orefaddress.orefdescription,
                )
            )
        self.connector = connector
        self.doc_url = doc_url

    def push(self):
        pass

    def delete(self):
        UtmRequest.delete(self.doc_url)
        return True

    def __str__(self):
        pass
