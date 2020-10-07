from generic.queries.utm import requests
from generic.helpers.textTransform import clean
from lxml import objectify as ob
from generic.exceptions import UnsupportedDocument, MissingArgument, TypeMismatch
from datetime import datetime


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
            r = requests.post(full_url, query)
            xml = ob.fromstring(clean(r))

            self.replyId = xml.url.text
            self.sign = xml.sign.text
            self.ok = r.ok

        elif self.doc_type == "QueryRestsShop_v2":
            full_url = f"{connector.base_url}/opt/in/QueryRestsShop_v2"
            query = {
                'xml_file': (
                    'QueryRestsShop.xml',
                    '<?xml version="1.0" encoding="UTF-8"?><ns:Documents Version="1.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:ns="http://fsrar.ru/WEGAIS/WB_DOC_SINGLE_01" xmlns:qp="http://fsrar.ru/WEGAIS/QueryParameters"><ns:Owner><ns:FSRAR_ID>' + connector.FSRAR + '</ns:FSRAR_ID></ns:Owner><ns:Document><ns:QueryRestsShop_v2></ns:QueryRestsShop_v2></ns:Document></ns:Documents>',
                    'application/xml'
                )
            }
            r = requests.post(full_url, query)
            xml = ob.fromstring(clean(r))
            self.replyId = xml.url.text
            self.sign = xml.sign.text
            self.ok = r.ok

        elif self.doc_type == "QueryRests":
            full_url = f"{connector.base_url}/opt/in/QueryRests"
            query = {
                'xml_file': (
                    'QueryParameters.xls',
                    '<?xml version="1.0" encoding="UTF-8"?><ns:Documents Version="1.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:ns="http://fsrar.ru/WEGAIS/WB_DOC_SINGLE_01" xmlns:qp="http://fsrar.ru/WEGAIS/QueryParameters"><ns:Owner><ns:FSRAR_ID>' + connector.FSRAR + '</ns:FSRAR_ID></ns:Owner><ns:Document><ns:QueryRests></ns:QueryRests></ns:Document></ns:Documents>',
                    'application/xml'
                )
            }
            r = requests.post(full_url, query)
            xml = ob.fromstring(clean(r))
            self.replyId = xml.url.text
            self.sign = xml.sign.text
            self.ok = r.ok

        elif self.doc_type == "TTN":
            full_url = f"{connector.base_url}/opt/in/QueryResendDoc"
            query = {
                'xml_file': (
                    'QueryParameters.xls',
                    '<?xml version="1.0" encoding="UTF-8"?><ns:Documents Version="1.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:ns="http://fsrar.ru/WEGAIS/WB_DOC_SINGLE_01" xmlns:qp="http://fsrar.ru/WEGAIS/QueryParameters"><ns:Owner><ns:FSRAR_ID>' + connector.FSRAR + '</ns:FSRAR_ID></ns:Owner><ns:Document><ns:QueryResendDoc><qp:Parameters><qp:Parameter><qp:Name>WBREGID</qp:Name><qp:Value>' +
                    kwargs[
                        'TTN'] + '</qp:Value></qp:Parameter></qp:Parameters></ns:QueryResendDoc></ns:Document></ns:Documents>',
                    'application/xml'
                )
            }
            r = requests.post(full_url, query)
            xml = ob.fromstring(clean(r))
            self.replyId = xml.url.text
            self.sign = xml.sign.text
            self.ok = r.ok

        elif self.doc_type == "TransferToShop":
            if not ('positions' in kwargs):
                raise MissingArgument("Missing positions list")
            if not type(kwargs['positions']) is list:
                raise TypeMismatch(f"Positions must be <class 'list'>. Current type is: {type(kwargs['positions'])}")

            full_url = f"{connector.base_url}/opt/in/TransferToShop"

            xml = [
                f'''<?xml version="1.0" encoding="utf-8"?>
<ns:Documents Version="1.0" xmlns:ns="http://fsrar.ru/WEGAIS/WB_DOC_SINGLE_01" xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:c="http://fsrar.ru/WEGAIS/Common" xmlns:pref="http://fsrar.ru/WEGAIS/ProductRef_v2" xmlns:tts="http://fsrar.ru/WEGAIS/TransferToShop">
  <ns:Owner>
    <ns:FSRAR_ID>{connector.FSRAR}</ns:FSRAR_ID>
  </ns:Owner>
  <ns:Document>
    <ns:TransferToShop>
      <tts:Identity>1/1</tts:Identity>
      <tts:Header>
        <tts:TransferNumber>{kwargs['number']}</tts:TransferNumber>
        <tts:TransferDate>{datetime.now().strftime("%Y-%m-%d")}</tts:TransferDate>
      </tts:Header>
      <tts:Content>''',
                [],
                '''</tts:Content>
    </ns:TransferToShop>
  </ns:Document>
</ns:Documents>''',
            ]
            i = 0
            for pos in kwargs['positions']:
                i = i+1
                xml[1].append(f'''<tts:Position>
          <tts:Identity>{i}</tts:Identity>
          <tts:ProductCode>{pos[0]}</tts:ProductCode>
          <tts:Quantity>{pos[1]}</tts:Quantity>
          <tts:InformF2>
            <pref:F2RegId>{pos[2]}</pref:F2RegId>
          </tts:InformF2>
        </tts:Position>''')
            xml[1] = ''.join(xml[1])
            query = {
                'xml_file': (
                    'TransferToShop.xml',
                    ''.join(xml),
                    'application/xml'
                )
            }

            r = requests.post(full_url, query)
            xml = ob.fromstring(clean(r))
            self.replyId = xml.url.text
            self.sign = xml.sign.text
            self.ok = r.ok

        else:
            raise UnsupportedDocument

    def __str__(self):
        return f"<{self.doc_type} [{self.ok}]>"
