import unittest

from fastapi.testclient import TestClient

from main import app


class ReverseEndpointTests(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_reverses_text(self):
        response = self.client.get("/reverse", params={"text": "hello"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"reversed": "olleh"})

    def test_accepts_empty_text(self):
        response = self.client.get("/reverse", params={"text": ""})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"reversed": ""})

    def test_requires_text(self):
        response = self.client.get("/reverse")

        self.assertEqual(response.status_code, 422)


if __name__ == "__main__":
    unittest.main()