from generic.documents.rests.rest import Rest
from generic.helpers.positions import Position
import datetime
from generic.queries.utm import requests


class ShopRest(Rest):
    def __init__(self, connector, xml_data, doc_url):
        self.Position = []
        self.RestDate = datetime.datetime.strptime(
            xml_data.nsDocument.nsReplyRestsShop_v2.rstRestsDate.text,
            "%Y-%m-%dT%H:%M:%S.%f"
        )
        if hasattr(xml_data.nsDocument.nsReplyRestsShop_v2.rstProducts, 'rstShopPosition'):
            for good in xml_data.nsDocument.nsReplyRestsShop_v2.rstProducts.rstShopPosition:
                if not hasattr(good.rstProduct.prefProducer, 'orefUL'):
                    producerClientRegId = good.rstProduct.prefProducer.orefFO.orefClientRegId.text
                    producerINN = None
                    producerKPP = None
                    producerFullName = good.rstProduct.prefProducer.orefFO.orefFullName.text
                    producerShortName = good.rstProduct.prefProducer.orefFO.orefShortName.text
                    addressCountry = good.rstProduct.prefProducer.orefFO.orefaddress.orefCountry.text
                    addressRegionCode = None
                    addressdescription = good.rstProduct.prefProducer.orefFO.orefaddress.orefdescription.text
                else:
                    producerClientRegId = good.rstProduct.prefProducer.orefUL.orefClientRegId.text
                    producerINN = good.rstProduct.prefProducer.orefUL.orefINN.text
                    producerKPP = good.rstProduct.prefProducer.orefUL.orefKPP.text
                    producerFullName = good.rstProduct.prefProducer.orefUL.orefFullName.text
                    producerShortName = good.rstProduct.prefProducer.orefUL.orefShortName.text
                    addressCountry = good.rstProduct.prefProducer.orefUL.orefaddress.orefCountry.text
                    addressRegionCode = good.rstProduct.prefProducer.orefUL.orefaddress.orefRegionCode.text
                    addressdescription = good.rstProduct.prefProducer.orefUL.orefaddress.orefdescription.text
                self.Position.append(
                    Position(
                        'ShopRests_v2',
                        ShopPositionQuantity=good.rstQuantity.text,
                        ProductFullName=good.rstProduct.prefFullName.text,
                        ProductAlcCode=good.rstProduct.prefAlcCode.text,
                        ProductCapacity=float(getattr(good.rstProduct, 'prefCapacity', 0)),
                        ProductUnitType=good.rstProduct.prefUnitType.text,
                        ProductAlcVolume=float(good.rstProduct.prefAlcVolume),
                        ProductVCode=good.rstProduct.prefProductVCode.text,
                        ProducerClientRegId=producerClientRegId,
                        ProducerINN=producerINN,
                        ProducerKPP=producerKPP,
                        ProducerFullName=producerFullName,
                        ProducerShortName=producerShortName,
                        addressCountry=addressCountry,
                        addressRegionCode=addressRegionCode,
                        addressdescription=addressdescription,
                    )
                )
        self.connector = connector
        self.doc_url = doc_url

    def push(self):
        pass

    def delete(self):
        requests.delete(self.doc_url)
        return True

    def __str__(self):
        return f"<{self.RestDate}, [{self.doc_url}]>"

    def write_off(self):
        pass
