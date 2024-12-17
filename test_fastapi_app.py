import unittest
from fastapi.testclient import TestClient
from fastapi_app import app
from unittest.mock import patch
import pandas as pd
from io import BytesIO

class TestFastAPI(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_read_root(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"Hello": "World"})

    @patch('requests.get')
    def test_get_natural_gas_prices(self, mock_get):
        # Create a small DataFrame
        df = pd.DataFrame({
          'Date': ['2021-01-01'],
          'Price': [2.5]
        })
        
        # Write the DataFrame to a BytesIO object as Excel
        excel_buffer = BytesIO()
        df.to_excel(excel_buffer, index=False, engine='openpyxl')
        mock_get.return_value.status_code = 200
        mock_get.return_value.content = excel_buffer.getvalue()
        
        response = self.client.get("/natural_gas_prices")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)
        self.assertEqual(response.json(), [{"Date": "2021-01-01", "Price": 2.5}])  # Expected structure