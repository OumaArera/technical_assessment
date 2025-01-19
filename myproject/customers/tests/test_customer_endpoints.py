from rest_framework import status  # type: ignore
from rest_framework.reverse import reverse  # type: ignore
from myproject.test_setup import GlobalAPITestCase
import json
from urllib.parse import urlencode


class UserViewTests(GlobalAPITestCase):
    def test_create_user_success(self):
        """Test creating a new user successfully."""
        test_user = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "johndoe@example.com",
            "username": "johndoe",
            "password": "John123#",
            "phone_number": "+254748800717",
        }

        endpoint = reverse('users')
        response = self.client.post(endpoint, test_user, format='json')
        # print("Response:", json.dumps(response.data,indent=2))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_user_invalid_data(self):
        """Test creating a user with invalid data."""
        test_user = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "com.example@johndoe", # Invalid email
            "username": "johndoe",
            "password": "Johndoeh", # Weak password
            "phone_number": "748800717", # Invalid phone number
        }

        endpoint = reverse('users')
        response = self.client.post(endpoint, test_user, format='json')
        # print("Response:", json.dumps(response.data,indent=2))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_get_user_by_id_success(self):
        """Test fetching a user by valid user ID."""
        endpoint = reverse('user-details', kwargs={"user_id": 1})
        response = self.client.get(endpoint, format='json')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        # print("Response:", json.dumps(response.data,indent=2))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_user_by_invalid_id(self):
        """Test fetching a user by invalid user ID."""
        endpoint = reverse('user-details', kwargs={"user_id": 9999})
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.get(endpoint, format='json')
        # print("Response:", json.dumps(response.data,indent=2))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_all_users(self):
        """Test fetching all users."""
        endpoint = reverse('users')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.get(endpoint, format='json')
        # print("Response:", json.dumps(response.data,indent=2))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_users_with_query_params(self):
        """Test fetching users with query parameters."""
        endpoint = f"{reverse('users')}?{urlencode({'customer_code':'Test124'})}"
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.get(endpoint, format='json')
        # print("Response:", json.dumps(response.data,indent=2))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_user_success(self):
        """Test updating a user successfully."""
        test_user_update = {
            "first_name": "John Updated",
            "phone_number": "+254745800715",
        }
        endpoint = reverse('user-details', kwargs={"user_id": 1})
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.put(endpoint, test_user_update, format='json')
        # print("Response:", json.dumps(response.data,indent=2))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_user_invalid_data(self):
        """Test updating a user with invalid data."""
        test_user_update = {
            "phone_number": "invalid-phone",
        }
        endpoint = reverse('user-details', kwargs={"user_id": 1})
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.put(endpoint, test_user_update, format='json')
        # print("Response:", json.dumps(response.data,indent=2))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_nonexistent_user(self):
        """Test updating a user that does not exist."""
        test_user_update = {
            "name": "Nonexistent User",
        }
        endpoint = reverse('user-details', kwargs={"user_id": 9999})
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.put(endpoint, test_user_update, format='json')
        # print("Response:", json.dumps(response.data,indent=2))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_user_success(self):
        """Test deleting a user successfully."""
        endpoint = reverse('user-details', kwargs={"user_id": 1})
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.delete(endpoint, format='json')
        # print("Response:", json.dumps(response.data,indent=2))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_nonexistent_user(self):
        """Test deleting a user that does not exist."""
        endpoint = reverse('user-details', kwargs={"user_id": 9999})
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.delete(endpoint, format='json')
        # print("Response:", json.dumps(response.data,indent=2))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
