from unittest import TestCase

from app import app


class CurrencyConversionTests(TestCase):
    def test_request(self):
        with app.test_client() as client:
            res = client.get("/")
            self.assertEqual(res.status_code, 200)

    def test_valid_conversion_request(self):
        with app.test_client() as client:
            res = client.post(
                "/convert_me",
                data={
                    "input_currency": "USD",
                    "output_currency": "EUR",
                    "amount": "100",
                },
            )
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"Successfully converted!", res.data)

    def test_invalid_currency_conversion_request(self):
        with app.test_client() as client:
            res = client.post(
                "/convert_me",
                data={
                    "input_currency": "USD",
                    "output_currency": "ASD",
                    "amount": "100",
                },
            )
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"Not a valid code: ASD", res.data)

    def test_invalid_amount_conversion_request(self):
        with app.test_client() as client:
            res = client.post(
                "/convert_me",
                data={
                    "input_currency": "USD",
                    "output_currency": "EUR",
                    "amount": "-100",
                },
            )
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"Not a valid amount: -100", res.data)
