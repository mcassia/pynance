import requests
import datetime
import math
from price import Price
import yahoo


class Ticker:

    def __init__(self, symbol):
        """
        Initialises a ticker given its symbol.

        Raises
        ------
            TickerException
                If the given symbol cannot uniquely identify a ticker.
        """
        self.symbol = symbol
        validateSymbol(symbol)

    def __repr__(self):
        return f'Ticker(symbol={self.symbol})'

    def getHistory(self, startDate, endDate):

        """
        Returns the price at market close for the ticker for each of the dates in the specified
        interval.

        Return
        ------
            dict[datetime.date: Price]
        """

        dateToTimestamp = lambda date: int(datetime.datetime(date.year, date.month, date.day).timestamp())
        timestampToDate = lambda timestamp: datetime.datetime.fromtimestamp(timestamp).date()

        URL = f'https://query1.finance.yahoo.com/v8/finance/chart/{self.symbol}?symbol={self.symbol}&period1={dateToTimestamp(startDate)}&period2={dateToTimestamp(endDate)}&useYfid=true&interval=1d&includePrePost=true&events=div%7Csplit%7Cearn&lang=en-GB&region=GB&crumb=1Lstoua9nzX&corsDomain=uk.finance.yahoo.com'
        response = yahoo.sendRequest(URL)

        currency = response['chart']['result'][0]['meta']['currency']

        timestamps = response['chart']['result'][0]['timestamp']
        dates = map(timestampToDate, timestamps)

        values = response['chart']['result'][0]['indicators']['quote'][0]['close']

        # Somehow, sometimes, the last value provided is multiplied by a power of 10; the below
        # attempts to detect when this occurs and corrects it. This would fail if the assumption
        # that a daily market price could increase by one or more order of magnitudes does not
        # hold (BTC I'm looking at you). This is a temporary remediation until more insight into
        # the issue is obtained.
        gap = round(math.log10(values[-1] / values[-2]))
        values[-1] /= (10 ** gap)        

        return dict(zip(dates, map(lambda value: Price(value, currency), values)))




class TickerException(Exception):

    """Raised when validation of a ticker symbol fails."""


class TickerNotFoundException(TickerException):

    """Raised when a symbol cannot be matched against any ticker."""

    def __init__(self, symbol):
        super().__init__(f'No ticker could be found with symbol \'{symbol}\'.')


class AmbiguousTickerException(TickerException):

    """Raised when a symbol being validated cannot uniquely identify one single ticker."""

    def __init__(self, symbol, foundSymbols):
        super().__init__(f'More than one ticker was found for symbol \'{symbol}\' ({sorted(foundSymbols)}).')


def validateSymbol(symbol, allowMismatchIfOne=False):

    """
    Given a ticker symbol, it determines whether it exists and if its unambiguous and raises
    an exception if the validation fails.

    Paramters
    ---------
        symbol: str
            The ticker symbol to validate
        allowMismatchIfOne: bool
            It determines whether validation should succeed if a single ticker is found for the
            given symbol, even if it does not match.

    Raise
    -----
        TickerNotFoundException
            If no ticker was found to match the given symbol
        AmbiguousTickerException
            If multiple tickers are found for the given symbol and the given symbol is not one of
            them or if a single one is found, but it does not match the given one (provided that
            the 'allowMismatchIfOne' is not set).
    """

    URL = f'https://query1.finance.yahoo.com/v1/finance/search?q={symbol}&lang=en-US&region=US&quotesCount=10'
    response = yahoo.sendRequest(URL)

    foundSymbols = set(map(lambda quote: quote['symbol'], response.get('quotes', [])))

    if not foundSymbols:
        raise TickerNotFoundException(symbol)
    elif len(foundSymbols) > 1:
        if symbol not in foundSymbols:
            raise AmbiguousTickerException(symbol, foundSymbols)
    else:
        foundSymbol = list(foundSymbols)[0]
        if foundSymbol != symbol and not allowMismatchIfOne:
            raise AmbiguousTickerException(symbol, [foundSymbol])


