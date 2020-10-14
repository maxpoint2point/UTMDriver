#  Copyright (c) maxpoint2point@gmail.com 2020.

import re
import html


def clean(raw):
    raw = raw.text.replace("""<?xml version="1.0" encoding="UTF-8" standalone="no"?>""", '')
    raw = raw.replace("""<?xml version="1.0" encoding="utf-8" standalone="no"?>""", '')
    raw = raw.replace("""<?xml version="1.0" encoding="utf-8"?>""", '')
    raw = raw.replace("""<?xml version="1.0" encoding="UTF-8"?>""", '')
    raw = re.sub(r'(?<=\w):(?=\w[^<>]*>)(?!\w+=)', '', raw)
    return raw


def getType(full_url):
    return re.split(r'/', full_url)[-2]


def unescape(text):
    return html.unescape(text)
