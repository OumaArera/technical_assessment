from unittest.mock import patch
from django.test import TestCase
from rest_framework.test import APIClient

class Auth0TestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.test_token = "mocked-auth0-token"
        self.auth_headers = {"HTTP_AUTHORIZATION": f"Bearer {self.test_token}"}

    @patch("auth_service.token_utils.validate_token")
    def test_signup(self, mock_validate_token):
        mock_validate_token.return_value = {
            "email": "testuser@example.com",
            "email_verified": True,
        }

        response = self.client.post(
            "/auth_service/signup/",
            data={"email": "testuser@example.com"},
            **self.auth_headers,
        )
        self.assertEqual(response.status_code, 201)

    @patch("auth_service.token_utils.validate_token")
    def test_login(self, mock_validate_token):
        mock_validate_token.return_value = {
            "email": "testuser@example.com",
            "email_verified": True,
        }

        response = self.client.post(
            "/auth_service/login/",
            **self.auth_headers,
        )
        self.assertEqual(response.status_code, 200)

    @patch("auth_service.token_utils.validate_token")
    def test_logout(self, mock_validate_token):
        mock_validate_token.return_value = {
            "email": "testuser@example.com",
            "email_verified": True,
        }

        response = self.client.post(
            "/auth_service/logout/",
            **self.auth_headers,
        )
        self.assertEqual(response.status_code, 204)
