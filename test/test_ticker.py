from datetime import date, datetime
from unittest import TestCase
import mock
from price import Price
from ticker import Ticker, validateSymbol, AmbiguousTickerException, TickerNotFoundException


class TestTicker(TestCase):
    
    def test_getPrice(self):

        """Validate that a ticker's history can be retreieved."""

        response = {
            'chart': {
                'result': [
                    {
                        'meta': {'currency': 'GBP', 'regularMarketPrice': 42.17},
                    },
                ]
            }
        }

        with mock.patch('yahoo.sendRequest', return_value=response), mock.patch('ticker.validateSymbol'):

            self.assertEquals(
                Ticker('YEET').getPrice(),
                Price(42.17, 'GBP')
            )

    def test_getHistory(self):

        """Validate that a ticker's history can be retreieved."""

        response = {
            'chart': {
                'result': [
                    {
                        'meta': {'currency': 'GBP'},
                        'timestamp': [1638101809, 1638188191, 1638274561],
                        'indicators': {'quote': [{'close': [1, 2, 3]}]}
                    },
                ]
            }
        }

        with mock.patch('yahoo.sendRequest', return_value=response), mock.patch('ticker.validateSymbol'):

            self.assertEquals(
                Ticker('YEET').getHistory(date(2021, 11, 28), date(2021, 11, 30)),
                {
                    date(2021, 11, 28): Price(1, 'GBP'),
                    date(2021, 11, 29): Price(2, 'GBP'),
                    date(2021, 11, 30): Price(3, 'GBP'),
                }

            )


    def test_validation(self):

        """Tests various scenarios of validation of a ticker symbol."""

        responses = {
            'A': ['A'],
            'B': ['B', 'BB'],
            'C': ['CC',],
            'D': [],
        }

        def sendRequest(URL, *args, **kwargs):
            for symbol, quotes in responses.items():
                if URL == f'https://query1.finance.yahoo.com/v1/finance/search?q={symbol}&lang=en-US&region=US&quotesCount=10':
                    for quote in quotes:
                        return {'quotes': [{'symbol': quote}]}
            return {}


        with mock.patch('yahoo.sendRequest', sendRequest):

            # This should succeed, as the symbol 'A' uniquely maps to a ticker;
            validateSymbol('A')

            # This should succeed, as the symbol 'B' maps to multiple tickers, but one of them matches exactly;
            validateSymbol('B')

            # This should fail, as the symbol 'C' maps to no ticker matching the symbol exactly;
            with self.assertRaises(AmbiguousTickerException):
                validateSymbol('C')

            # This should succeed, as the symbol 'C' maps to no ticker matching the symbol exactly,
            # but exactly one is found and the provided parameter allows it;
            validateSymbol('C', allowMismatchIfOne=True)

            # This should fail, as the symbol 'D' maps to no ticker;
            with self.assertRaises(TickerNotFoundException):
                validateSymbol('D')


