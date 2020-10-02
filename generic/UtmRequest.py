import requests
from generic.exceptions import UTMNotConnect, DocumentNotFound


def get(url):
    try:
        r = requests.get(url)
    except requests.exceptions.ConnectionError:
        raise UTMNotConnect
    if r.status_code == 404:
        raise DocumentNotFound
    if r.status_code != 200:
        raise UTMNotConnect
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
