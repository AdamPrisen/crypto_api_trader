import os
import unittest
import json
from db import db
from app import app
from ma import ma
from models.exchange import ExchangeModel



SQLALCHEMY_DATABASE_URI = "sqlite:///test.db"
db.init_app(app)

class Tests(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
        with app.app_context():
            db.drop_all()
            db.create_all()
        self.app = app.test_client()

        
    def test_create_exchange(self):
        route = '/api/v1/crypto/exchanges'
        headers = {"Content-Type": "application/json"}
        
        #check valid data
        payload = json.dumps({
            "name":"zmenaren",
            "currency": "eur"
        })
        response = self.app.post(
            route,
            headers = headers,
            data=payload
        )
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(201, response.status_code)
        self.assertEqual('zmenaren', data['name'])

        #check invalid name data
        payload = json.dumps({
            "name": "",
            "currency": "eur"
        })
        response = self.app.post(
            route,
            headers=headers,
            data=payload
        )
        self.assertEqual(400, response.status_code)

        #check invalid currency data
        payload = json.dumps({
            "name": "zmenaren02",
            "currency": ".."
        })
        response = self.app.post(
            route,
            headers=headers,
            data=payload
        )
        self.assertEqual(400, response.status_code)

        #check duplicate name
        payload = json.dumps({
            "name": "zmenaren02",
            "currency": "j"
        })
        response = self.app.post(
            route,
            headers=headers,
            data=payload
        )
        self.assertEqual(400, response.status_code)

    
    def test_deposit(self):
        route = '/api/v1/crypto/exchanges'
        headers = {"Content-Type": "application/json"}

        #create first exchange
        payload = json.dumps({
            "name": "zmenaren",
            "currency": "eur"
        })
        response = self.app.post(
            route,
            headers=headers,
            data=payload
        )
        self.assertEqual(201, response.status_code)

        route = '/api/v1/crypto/exchanges/1'
        #valid deposit
        payload = json.dumps({
            "amount": 1000,
        })
        response = self.app.post(
            route,
            headers=headers,
            data=payload
        )
        self.assertEqual(200, response.status_code)

        #invalid deposit
        payload = json.dumps({
            "amount": 0,
        })
        response = self.app.post(
            route,
            headers=headers,
            data=payload
        )
        self.assertEqual(400, response.status_code)

    def test_cryptocncy(self):
        #make exchage
        route = '/api/v1/crypto/exchanges'
        headers = {"Content-Type": "application/json"}

        payload = json.dumps({
            "name": "zmenaren",
            "currency": "eur"
        })
        response = self.app.post(
            route,
            headers=headers,
            data=payload
        )
        self.assertEqual(201, response.status_code)

        #make valid cryptocurrency
        route = '/api/v1/crypto/exchanges/1/currencie'
        payload = json.dumps({
            "shortcut": "btc",
            "rate": 10000
        })
        response = self.app.put(
            route,
            headers=headers,
            data=payload
        )
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(201, response.status_code)
        self.assertEqual(10000, data['cryptocurrencies'][0]['rate'])

        #update currency
        payload = json.dumps({
            "shortcut": "btc",
            "rate": 100
        })
        response = self.app.put(
            route,
            headers=headers,
            data=payload
        )
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(201, response.status_code)
        self.assertEqual(100, data['cryptocurrencies'][0]['rate'])

        #delete currencie
        payload = json.dumps({
            "shortcut": "btc",
            "delete": True
        })
        response = self.app.put(
            route,
            headers=headers,
            data=payload
        )
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(200, response.status_code)
        self.assertEqual([], data['cryptocurrencies'])

        #make valid currencie
        payload = json.dumps({
            "shortcut": "btc",
            "rate": -1
        })
        response = self.app.put(
            route,
            headers=headers,
            data=payload
        )
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(400, response.status_code)

    def test_trade_and_hystory(self):
        #make exchange
        route = '/api/v1/crypto/exchanges'
        headers = {"Content-Type": "application/json"}

        payload = json.dumps({
            "name": "zmenaren",
            "currency": "eur"
        })
        response = self.app.post(
            route,
            headers=headers,
            data=payload
        )
        self.assertEqual(201, response.status_code)

        #make 2 cryptocurrencies
        route = '/api/v1/crypto/exchanges/1/currencie'
        payload = json.dumps({
            "shortcut": "btc",
            "rate": 10000
        })
        response = self.app.put(
            route,
            headers=headers,
            data=payload
        )
        self.assertEqual(201, response.status_code)

        payload = json.dumps({
            "shortcut": "btb",
            "rate": 1000
        })
        response = self.app.put(
            route,
            headers=headers,
            data=payload
        )
        self.assertEqual(201, response.status_code)

        #deposit on exchange
        route = '/api/v1/crypto/exchanges/1'
        payload = json.dumps({
            "amount": 10000
        })
        response = self.app.post(
            route,
            headers=headers,
            data=payload
        )
        self.assertEqual(200, response.status_code)

        #make valid trade from main currency to cryptocurrency
        route = '/api/v1/crypto/exchanges/1/trades'
        payload = json.dumps({
            "amount": 10000,
            "currency_in": "eur",
            "currency_out": "btc"
        })
        response = self.app.post(
            route,
            headers=headers,
            data=payload
        )
        self.assertEqual(201, response.status_code)

        #make valid trade from cryptocurrency to cryptocurrency
        payload = json.dumps({
            "amount": 0.5,
            "currency_in": "btc",
            "currency_out": "btb"
        })
        response = self.app.post(
            route,
            headers=headers,
            data=payload
        )
        self.assertEqual(201, response.status_code)

        #make valid trade from cryptocurrency to main currency
        payload = json.dumps({
            "amount": 4,
            "currency_in": "btb",
            "currency_out": "eur"
        })
        response = self.app.post(
            route,
            headers=headers,
            data=payload
        )
        self.assertEqual(201, response.status_code)

        #make invalid trades --lack of resources
        payload = json.dumps({
            "amount": 1.1,
            "currency_in": "btb",
            "currency_out": "eur"
        })
        response = self.app.post(
            route,
            headers=headers,
            data=payload
        )
        self.assertEqual(400, response.status_code)

        payload = json.dumps({
            "amount": 0.6,
            "currency_in": "btc",
            "currency_out": "btb"
        })
        response = self.app.post(
            route,
            headers=headers,
            data=payload
        )
        self.assertEqual(400, response.status_code)

        payload = json.dumps({
            "amount": 4001,
            "currency_in": "eur",
            "currency_out": "btc"
        })
        response = self.app.post(
            route,
            headers=headers,
            data=payload
        )
        self.assertEqual(400, response.status_code)

        #check valid trades history
        route = "/api/v1/crypto/history"
        response = self.app.get(
            route,
            headers=headers,
        )
        data = json.loads(response.get_data())['trades']
        self.assertEqual(200, response.status_code)
        self.assertEqual(3, len(data))

        route = "/api/v1/crypto/history?search=eur"
        response = self.app.get(
            route,
            headers=headers,
        )
        data = json.loads(response.get_data())['trades']
        self.assertEqual(200, response.status_code)
        self.assertEqual(2, len(data))

        route = "/api/v1/crypto/history?search=eur&limit=1"
        response = self.app.get(
            route,
            headers=headers,
        )
        data = json.loads(response.get_data())['trades']
        self.assertEqual(200, response.status_code)
        self.assertEqual(1, len(data))

        route = "/api/v1/crypto/history?search=eur&limit=1&offset=2"
        response = self.app.get(
            route,
            headers=headers,
        )
        data = json.loads(response.get_data())['trades']
        self.assertEqual(200, response.status_code)
        self.assertEqual(0, len(data))


if __name__ == '__main__':
    unittest.main()
