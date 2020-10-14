#  Copyright (c) maxpoint2point@gmail.com 2020.

from UTMDriver.generic.queries.utm import requests
from UTMDriver.generic.helpers.textTransform import clean
from lxml import objectify as ob
from UTMDriver.generic.exceptions import UnsupportedDocument, MissingArgument, TypeMismatch
from datetime import datetime
import jinja2


class Request:
    replyId = None
    sign = None
    ok = None
    doc_type = None

    def __init__(self, connector, doc_type, **kwargs):
        self.doc_type = doc_type

        templateLoader = jinja2.FileSystemLoader(searchpath="UTMDriver/generic/queries/documents/templates/")
        templateEnv = jinja2.Environment(loader=templateLoader, autoescape=True)
        template = templateEnv.get_template(f'{doc_type}.xml')

        # Запрос неподтвержденных накладных
        if self.doc_type == "QueryNATTN":
            full_url = f"{connector.base_url}/opt/in/QueryNATTN"
            outputText = template.render(fsrar=connector.FSRAR)
            query = {
                'xml_file': (
                    'QueryNATTN.xml',
                    outputText,
                    'application/xml'
                )
            }
            r = requests.post(full_url, query)
            xml = ob.fromstring(clean(r))

            self.replyId = xml.url.text
            self.sign = xml.sign.text
            self.ok = r.ok

        # Запрос остатков в регистре №2
        elif self.doc_type == "QueryRestsShop_v2":
            full_url = f"{connector.base_url}/opt/in/QueryRestsShop_v2"
            outputText = template.render(fsrar=connector.FSRAR)
            query = {
                'xml_file': (
                    'QueryRestsShop.xml',
                    outputText,
                    'application/xml'
                )
            }
            r = requests.post(full_url, query)
            xml = ob.fromstring(clean(r))
            self.replyId = xml.url.text
            self.sign = xml.sign.text
            self.ok = r.ok

        # Запрос остатков в регистре №1
        elif self.doc_type == "QueryRests":
            full_url = f"{connector.base_url}/opt/in/QueryRests"
            outputText = template.render(fsrar=connector.FSRAR)
            query = {
                'xml_file': (
                    'QueryParameters.xls',
                    outputText,
                    'application/xml'
                )
            }
            r = requests.post(full_url, query)
            xml = ob.fromstring(clean(r))
            self.replyId = xml.url.text
            self.sign = xml.sign.text
            self.ok = r.ok

        # Запрос накладной
        elif self.doc_type == "QueryResendDoc":
            full_url = f"{connector.base_url}/opt/in/QueryResendDoc"
            outputText = template.render(fsrar=connector.FSRAR, ttn=kwargs['TTN'])
            query = {
                'xml_file': (
                    'QueryParameters.xls',
                    outputText,
                    'application/xml'
                )
            }
            r = requests.post(full_url, query)
            xml = ob.fromstring(clean(r))
            self.replyId = xml.url.text
            self.sign = xml.sign.text
            self.ok = r.ok

        # Передача алкогольной продукции в регистр №2
        elif self.doc_type == "TransferToShop":
            if not ('positions' in kwargs):
                raise MissingArgument("Missing positions list")
            if not type(kwargs['positions']) is dict:
                raise TypeMismatch(f"Positions must be <class 'dict'>. Current type is: {type(kwargs['positions'])}")
            if not ('number' in kwargs):
                raise MissingArgument("Missing number")

            full_url = f"{connector.base_url}/opt/in/TransferToShop"
            outputText = template.render(
                fsrar=connector.FSRAR,
                positions=kwargs['positions'],
                number=kwargs['number'],
                date=datetime.now().strftime("%Y-%m-%d")
            )
            query = {
                'xml_file': (
                    'TransferToShop.xml',
                    outputText,
                    'application/xml'
                )
            }

            r = requests.post(full_url, query)
            xml = ob.fromstring(clean(r))
            self.replyId = xml.url.text
            self.sign = xml.sign.text
            self.ok = r.ok

        # Списания алкогольной продукции из регистра №2
        elif self.doc_type == "ActWriteOfShop_v2":
            if not ('positions' in kwargs):
                raise MissingArgument("Missing positions list")
            if not type(kwargs['positions']) is list:
                raise TypeMismatch(f"Positions must be <class 'list'>. Current type is: {type(kwargs['positions'])}")
            if not ('number' in kwargs):
                raise MissingArgument("Missing number")
            if not ('reason' in kwargs):
                raise MissingArgument("Missing reason")
            good_reason = {
                'Пересортица',
                'Недостача',
                'Уценка',
                'Порча',
                'Потери',
                'Проверки',
                'Арест',
                'Иные цели',
                'Реализация',
                'Производственные потери',
            }
            if not kwargs['reason'] in good_reason:
                raise TypeMismatch(f"The reason must be from the list: {good_reason}")

            full_url = f"{connector.base_url}/opt/in/ActWriteOffShop_v2"

            outputText = template.render(
                fsrar=connector.FSRAR,
                reason=kwargs['reason'],
                number=kwargs['number'],
                date=datetime.now().strftime("%Y-%m-%d"),
                positions=kwargs['positions'],
            )

            query = {
                'xml_file': (
                    'ActWriteOfShopv2.xml',
                    outputText,
                    'application/xml'
                )
            }

            r = requests.post(full_url, query)
            xml = ob.fromstring(clean(r))
            self.replyId = xml.url.text
            self.sign = xml.sign.text
            self.ok = r.ok

        elif self.doc_type == 'WayBillAct_v3':
            if not ('number' in kwargs):
                raise MissingArgument("Missing number")
            if not ('ttn_id' in kwargs):
                raise MissingArgument("Missing ttn_id")

            full_url = f"{connector.base_url}/opt/in/WayBillAct_v3"
            outputText = template.render(
                fsrar=connector.FSRAR,
                ttn_id=kwargs['ttn_id'],
                number=kwargs['number'],
                date=datetime.now().strftime("%Y-%m-%d")
            )
            query = {
                'xml_file': (
                    'WayBillAct_v3.xml',
                    outputText,
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

    def __bool__(self):
        return self.ok
