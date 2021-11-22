from currency import getExchangeRate


class Price(object):

    """Represents a price in monetary terms, defined by a numeric value and a currency."""

    def __init__(self, value: float, currency: str):
        """
        Initialises the price object given the amount value and the currency.

        Parameters
        ----------
            value: float
            currency: str
        """
        self.value = value
        self.currency = currency

    def __repr__(self) -> str:
        return f'{self.value} {self.currency}'

    def __hash__(self):
        return hash((self.value, self.currency))

    def __eq__(self, other):
        return hash(self) == hash(other)

    def convert(self, currency, date=None):
        """
        Converts the price into a different currency, optionally for the exchange
        rate of a past date, if available.

        Parameters
        ----------
            currency: str
            date: datetime.date

        Return
        ------
            Price

        Example
        -------
            >>> Price(1., 'USD').convert('GBP', date=datetime.date(2010, 5, 7))
            0.74 GBP
        """
        return Price(self.value * getExchangeRate(self.currency, currency, date=date), currency)
