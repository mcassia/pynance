import datetime
from unittest import TestCase
from order import Order, OrderDirection, Orders
import json
from price import Price


class TestOrders(TestCase):
    
    def test_fromJSON(self):

        text = json.dumps(
            [
                {
                    "symbol": "SWDA.L",
                    "direction": "buy",
                    "quantity": 7,
                    "price": {
                        "value": 56.69,
                        "currency": "GBP"
                    },
                    "fee": {
                        "value": 6,
                        "currency": "GBP"
                    },
                    "date": "2021-01-01"
                }
            ]
        )

        order = Order(
            symbol='SWDA.L',
            direction=OrderDirection.Buy,
            quantity=7,
            date=datetime.date(2021, 1, 1),
            price=Price(56.69, 'GBP'),
            fee=Price(6, 'GBP'),
        )

        self.assertEquals(Orders.fromJSON(text), Orders([order]))


