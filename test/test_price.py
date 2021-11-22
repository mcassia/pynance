from datetime import date
from unittest import TestCase
from price import Price


class TestPrice(TestCase):

    def test_representPrice(self):
        self.assertEqual(str(Price(100, 'USD')), '100 USD')

    def test_convert(self):
        self.assertEqual(
            Price(1, 'USD').convert('GBP', date=date(2010, 5, 7)),
            Price(0.681037188137455, 'GBP')
        )
        