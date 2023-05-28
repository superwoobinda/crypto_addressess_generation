import json
import unittest
import coinaddrvalidator

from main import app, db


class TestView(unittest.TestCase):
    def setUp(self):
        self.ctx = app.app_context()
        self.ctx.push()
        self.client = app.test_client()
        db.create_all()

    def tearDown(self):
        db.drop_all()

    def test_generate_btc_address(self):
        data = {'acronym': 'BTC'}
        response = self.client.post('/generate_address', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        btc_address = json.loads(response.get_data(as_text=True)).get('address')
        self.assertTrue(coinaddrvalidator.validate('btc', btc_address))

    def test_generate_eth_address(self):
        data = {'acronym': 'ETH'}
        response = self.client.post('/generate_address', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        eth_address = json.loads(response.get_data(as_text=True)).get('address')
        self.assertTrue(coinaddrvalidator.validate('ethereum', eth_address))

    def test_list_address(self):
        data = {'acronym': 'BTC'}
        self.client.post('/generate_address', data=json.dumps(data), content_type='application/json')
        data = {'acronym': 'ETH'}
        self.client.post('/generate_address', data=json.dumps(data), content_type='application/json')

        response = self.client.get('/list_address', content_type='application/json')
        self.assertEqual(response.status_code, 200)
        addresses = json.loads(response.get_data(as_text=True))
        self.assertEqual(len(addresses), 2)

    def test_retrieve_address(self):
        data = {'acronym': 'BTC'}
        self.client.post('/generate_address', data=json.dumps(data), content_type='application/json')

        response = self.client.get('/retrieve_address/1', content_type='application/json')
        self.assertEqual(response.status_code, 200)
        addresses = json.loads(response.get_data(as_text=True))
        btc_address_id = addresses.get("id")
        self.assertEqual(btc_address_id, 1)


if __name__ == "__main__":
    unittest.main()
