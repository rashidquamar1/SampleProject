import os
import tempfile
import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient

from auth_service.main import app


class AuthenticationEndpointTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.environment = patch.dict(
            os.environ,
            {
                "AUTH_DATABASE_PATH": f"{self.temp_dir.name}/users.db",
                "JWT_SECRET_KEY": "test-secret-key-with-at-least-32-characters",
            },
        )
        self.environment.start()
        self.client = TestClient(app)

    def tearDown(self):
        self.environment.stop()
        self.temp_dir.cleanup()

    def register_user(self, email="reader@example.com", password="correct-horse-42"):
        return self.client.post(
            "/auth/register",
            json={"email": email, "password": password},
        )

    def test_register_login_and_access_profile(self):
        registration = self.register_user()

        self.assertEqual(registration.status_code, 201)
        self.assertEqual(registration.json(), {"email": "reader@example.com"})

        login = self.client.post(
            "/auth/token",
            data={"username": "reader@example.com", "password": "correct-horse-42"},
        )

        self.assertEqual(login.status_code, 200)
        token = login.json()["access_token"]
        profile = self.client.get(
            "/users/me",
            headers={"Authorization": f"Bearer {token}"},
        )

        self.assertEqual(profile.status_code, 200)
        self.assertEqual(profile.json(), {"email": "reader@example.com"})

    def test_registration_rejects_duplicate_email_case_insensitively(self):
        self.assertEqual(self.register_user().status_code, 201)

        duplicate = self.register_user(email="READER@example.com")

        self.assertEqual(duplicate.status_code, 409)

    def test_login_rejects_incorrect_password(self):
        self.register_user()

        response = self.client.post(
            "/auth/token",
            data={"username": "reader@example.com", "password": "wrong-password"},
        )

        self.assertEqual(response.status_code, 401)

    def test_profile_requires_authentication(self):
        response = self.client.get("/users/me")

        self.assertEqual(response.status_code, 401)


if __name__ == "__main__":
    unittest.main()