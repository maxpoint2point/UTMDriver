import requests
import re
from lxml import objectify as ob


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

        requests.get('http://'+address+':'+port)

    def __clearResponse(self, response):
        """
        Очистка xml ответа от лишнего мусора
        """
        response = response.replace("""<?xml version="1.0" encoding="UTF-8" standalone="no"?>""", '')
        response = response.replace("""<?xml version="1.0" encoding="utf-8" standalone="no"?>""", '')
        response = response.replace("""<?xml version="1.0" encoding="utf-8"?>""", '')
        response = response.replace("""<?xml version="1.0" encoding="UTF-8"?>""", '')
        response = re.sub(r'(?<=\w):(?=\w[^<>]*>)(?!\w+=)', '', response)
        return response

    def getInboxDocuments(self):
        r = requests.get(self._url_out)
        xml = self.__clearResponse(r.text)
        return ob.fromstring(xml)