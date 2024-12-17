import unittest
from fastapi.testclient import TestClient
from fastapi_app import app
from unittest.mock import patch

class TestFastAPI(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_read_root(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"Hello": "World"})

    @patch('requests.get')
    def test_get_natural_gas_prices(self, mock_get):
        # Configure the mock to return a response with an OK status
        mock_get.return_value.status_code = 200
        mock_get.return_value.content = b"Some content"  # Mocked file content
        
        response = self.client.get("/natural_gas_prices")
        self.assertEqual(response.status_code, 200)
        # Test that the response is a list
        self.assertIsInstance(response.json(), list)

if __name__ == '__main__':
    unittest.main()