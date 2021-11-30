from datetime import date, datetime
from unittest import TestCase
import mock
from yahoo import sendRequest


class TestYahoo(TestCase):

    def test_sendRequest(self):

        # Validate that the GET request is actually sent and not read from cache.
        with mock.patch('requests.get'), mock.patch('yahoo._doSendRequest') as send, mock.patch('yahoo._getCache') as cache:
            sendRequest('https://foo.com/api/v1/yeet', useCache=True)
            self.assertTrue(send.called)
            self.assertFalse(cache.called)

        # Validate that the GET request is not sent and instead the result is read from cache.
        with mock.patch('requests.get'), mock.patch('yahoo._doSendRequest') as send, mock.patch('yahoo._getCache') as cache:
            sendRequest('https://foo.com/api/v1/yeet', useCache=True)
            self.assertFalse(send.called)
            self.assertTrue(cache.called)

        # Validate that the GET request is actually sent even though cache is available, since the parameter requires it.
        with mock.patch('requests.get'), mock.patch('yahoo._doSendRequest') as send, mock.patch('yahoo._getCache') as cache:
            sendRequest('https://foo.com/api/v1/yeet', useCache=False)
            self.assertTrue(send.called)
            self.assertFalse(cache.called)
        