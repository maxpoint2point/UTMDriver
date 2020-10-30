#  Copyright (c) maxpoint2point@gmail.com 2020.

import requests
from ....generic.exceptions import UTMNotConnect, DocumentNotFound


def get(url):
    try:
        r = requests.get(url)
    except requests.exceptions.ConnectionError:
        raise UTMNotConnect(f"Unable to connect to UTM: [{url}]")
    if r.status_code == 404:
        raise DocumentNotFound(f"<Document with url: {url} [Not Found: 404]>")
    if r.status_code != 200:
        raise UTMNotConnect(f"UTM status is different from [200]. Current status is: [{r.status_code}]")
    return r


def post(url, files):
    try:
        r = requests.post(url, files=files)
    except requests.exceptions.ConnectionError:
        raise UTMNotConnect
    if r.status_code != 200:
        raise UTMNotConnect
    return r


def delete(url):
    try:
        r = requests.delete(url)
    except requests.exceptions.ConnectionError:
        raise UTMNotConnect
    if r.status_code != 200:
        raise UTMNotConnect
    return r
