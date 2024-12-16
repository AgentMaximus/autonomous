import unittest
from fastapi.testclient import TestClient
from app import app

class TestApp(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(app)

    def test_root(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("message", response.json())

    def test_health_check(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "healthy")

    def test_deep_health_check(self):
        response = self.client.get("/health/deep")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "healthy")

    def test_custom_error_404(self):
        response = self.client.get("/error/404")
        self.assertEqual(response.status_code, 404)

    def test_custom_error_401(self):
        response = self.client.get("/error/401")
        self.assertEqual(response.status_code, 401)

    def test_custom_error_403(self):
        response = self.client.get("/error/403")
        self.assertEqual(response.status_code, 403)

if __name__ == "__main__":
    unittest.main()