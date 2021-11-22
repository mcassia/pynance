import datetime
from unittest import TestCase
import currency


class TestCurrency(TestCase):

    def test_getCurrencyConverter(self):
        "Tests the ability to retrieve a global (singleton) instance of the currency converter."
        currency.CURRENCY_CONVERTER = None
        currencyConverter = currency._getCurrencyConverter()
        self.assertEqual(currencyConverter, currency.CURRENCY_CONVERTER, 'Once the currency converter is retrieved the first time, it should be stored in a global variable.')
        self.assertEqual(currencyConverter, currency._getCurrencyConverter(), 'Once the currency converter is requested a second time, it should return the original instance.')

    def test_getExchangeRate(self):
        """Tests the ability of retrieving the correct exchange rate (latest and for a date)
        and that it fails appropriately."""
        self.assertIsInstance(currency.getExchangeRate('USD', 'GBP'), float)
        self.assertEquals(currency.getExchangeRate('USD', 'GBP', date=datetime.date(2010, 5, 11)), 0.6769570011025359)
        with self.assertRaises(RuntimeError):
            _ = currency.getExchangeRate('USD', 'YEET')
        with self.assertRaises(RuntimeError):
            _ = currency.getExchangeRate('USD', 'GBP', date=datetime.date(1715, 12, 3))

    def test_download(self):
        try:
            _ = currency._CurrencyConverter.download()
        except Exception:
            self.fail('The converter failed to be initialised by download.')