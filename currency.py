from datetime import datetime
from io import BytesIO
from zipfile import ZipFile
from urllib.request import urlopen
from pandas import read_csv


CURRENCY_TABLE_URL = 'https://www.ecb.europa.eu/stats/eurofxref/eurofxref-hist.zip'
CURRENCY_FILE_NAME = 'eurofxref-hist.csv'
DATE_COLUMN_NAME = 'Date'
CURRENCY_CONVERTER = None


def getExchangeRate(baseCurrency: str, targetCurrency: str, date: datetime.date=None) -> float:

    """
    Given two currencies, it returns the exchange rate between the two,
    optionally for a specified date, if provided.

    Parameters
    ----------
        baseCurrency: str
        targetCurrency: str
        date: datetime.date

    Return
    ------
        float

    Example
    -------
        >>> getExchangeRate('USD', 'GBP')
        0.420
        >>> getExchangeRate('USD', 'GBP', date=datetime.date(2010, 5, 7))
        0.69
    """

    return _getCurrencyConverter().getExchangeRate(baseCurrency, targetCurrency, date=date)


def _getCurrencyConverter():
    global CURRENCY_CONVERTER
    if not CURRENCY_CONVERTER:
        CURRENCY_CONVERTER = _CurrencyConverter.download()
    return CURRENCY_CONVERTER


class _CurrencyConverter(object):

    @staticmethod
    def download():
        file = ZipFile(BytesIO(urlopen(CURRENCY_TABLE_URL).read()))
        table = read_csv(file.open(CURRENCY_FILE_NAME))
        table['EUR'] = 1.
        return _CurrencyConverter(table)

    def __init__(self, table):

        """
        Initialises the currency conversion converter given a conversion
        table.

        Parameters
        ----------
            table: pandas.DataFrame
                A table mapping the relative value of currencies by date.
        """

        self.table = table

    def getAvailableCurrencies(self):
        return set(self.table.columns) - {'Date',}

    def getExchangeRate(self, baseCurrency: str, targetCurrency: str, date: datetime.date=None) -> float:

        # Ensure the teo provided currencies are valid;
        for currency in (baseCurrency, targetCurrency):
            if currency not in self.getAvailableCurrencies():
                raise RuntimeError('Unknown currency %s.', currency)

        # Extract the records for the two currencies;
        table = self.table[[baseCurrency, targetCurrency, DATE_COLUMN_NAME]]
        table = table.sort_values(DATE_COLUMN_NAME)

        # Determine for which date the conversion must be made and ensure it's valid;
        date = date.strftime('%Y-%m-%d') if date else table.iloc[-1][DATE_COLUMN_NAME]
        table = table[table[DATE_COLUMN_NAME] == date].dropna()
        if len(table) != 1:
            raise RuntimeError('No exchange rate could be found for %s and %s on %s.', baseCurrency, targetCurrency, date)

        # Determine the exchange rate;
        entry = table.iloc[0]
        exchangeRate = entry[targetCurrency] / entry[baseCurrency]

        return exchangeRate