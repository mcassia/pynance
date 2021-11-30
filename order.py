
from enum import Enum
import json
from price import Price
import datetime
from ticker import Ticker


class OrderDirection(Enum):

    Buy = 'Buy'
    Sell = 'Sell'


class Order(object):

    def __init__(self, symbol, direction, quantity, price, date, fee=None):
        self.symbol = symbol
        self.direction = direction
        self.quantity = quantity
        self.price = price
        self.fee = fee
        self.date = date        

    def __hash__(self):
        return hash((self.symbol, self.direction, self.quantity, self.price, self.date, self.fee))

    def __eq__(self, order):
        return isinstance(order, Order) and hash(self) == hash(order)


class Orders(object):

    @staticmethod
    def fromFile(path):
        """
        Reads orders from a JSON file.
        
        The text must be in JSON format and formatted as follows:

            {
                symbol: string;
                quantity: number;
                direction: string;
                date: string;
                price: {
                    value: number;
                    currency: string;
                };
                fee?: {
                    value: number;
                    currency: string;
                };
            }[]

        Parameters
        ----------
            path: str

        Return
        ------
            Orders
        """
        return Orders.fromJSON(open(path, 'r').read())

    @staticmethod
    def fromJSON(text):

        """
        Reads orders from JSON text.
        
        The text must be in JSON format and formatted as follows:

            {
                symbol: string;
                quantity: number;
                direction: string;
                price: {
                    value: number;
                    currency: string;
                };
                fee?: {
                    value: number;
                    currency: string;
                };
            }[]

        Parameters
        ----------
            text: str

        Return
        ------
            Orders
        """

        orders = []

        for order in json.loads(text):
            orders.append(
                Order(
                    symbol=order['symbol'],
                    direction={'buy': OrderDirection.Buy, 'sell': OrderDirection.Sell}[order['direction']],
                    quantity=order['quantity'],
                    price=Price(value=order['price']['value'], currency=order['price']['currency']),
                    fee=Price(value=order['fee']['value'], currency=order['fee']['currency']) if order.get('fee') else None,
                    date=datetime.datetime.strptime(order['date'], '%Y-%m-%d').date()
                )
            )

        return Orders(orders)

    def __init__(self, orders):
        self.orders = orders

    def __hash__(self):
        return hash(tuple(self.orders))

    def __eq__(self, orders):
        return isinstance(orders, Orders) and hash(orders) == hash(self)