import requests


_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'
}

_CACHE = {}


def sendRequest(URL, useCache=True):

    """
    Sends an HTTP GET request to a Yahoo Finance REST API endpoint and returns its parsed JSON
    content.

    Parameters
    ----------
        URL: str
        useCache: bool

    Return
    ------
        object
    """

    global _CACHE

    if _hasCache(URL) and useCache:
        return _getCache(URL)
    else:
        response = _doSendRequest(URL)        
        _setCache(URL, response)
        return response    


def _doSendRequest(URL):
    return requests.get(URL, headers=_HEADERS).json()


def _getCache(URL):
    return _CACHE.get(URL)


def _setCache(URL, response):
    global _CACHE
    _CACHE[URL] = response


def _hasCache(URL):
    return URL in _CACHE