from rest_framework import status  # type: ignore
from rest_framework.reverse import reverse  # type: ignore
from myproject.test_setup import GlobalAPITestCase
import json


class LoginViewTests(GlobalAPITestCase):

    def test_login_success(self):
            """Test login user successfully."""
            test_user = {
                "username": "Ouma",
                "password": "Test1234#"
            }

            endpoint = reverse('auth')
            response = self.client.post(endpoint, test_user, format='json')
            # print("Response:", json.dumps(response.data,indent=2))
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_fail(self):
            """Test login user unsuccessfully."""
            test_user = {
                "username": "INVALID",
                "password": "Test1234#"
            }

            endpoint = reverse('auth')
            response = self.client.post(endpoint, test_user, format='json')
            # print("Response:", json.dumps(response.data,indent=2))
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_login_invalid_data(self):
            """Test login user unsuccessfully."""
            test_user = {
                "username": "",
                "password": ""
            }

            endpoint = reverse('auth')
            response = self.client.post(endpoint, test_user, format='json')
            # print("Response:", json.dumps(response.data,indent=2))
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)