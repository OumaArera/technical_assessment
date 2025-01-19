from urllib.parse import urlencode
from rest_framework import status  # type: ignore
from rest_framework.reverse import reverse  # type: ignore
from myproject.test_setup import GlobalAPITestCase
import json


class OrderViewTests(GlobalAPITestCase):
    def test_create_order_success(self):
        """Test creating a new order successfully."""
        test_order = {
            "customer_code": "Test123",
            "price": 100,
            "item": "Shoes 1",
        }

        endpoint = reverse('orders')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.post(endpoint, test_order, format='json')
        # print("Response:", json.dumps(response.data, indent=2))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_order_invalid_data(self):
        """Test creating an order with invalid data."""
        test_order = {
            "customer_code": "", #Invalid customer code
            "price": None, # Invalid price
            "item": "Shoes 1",
        }

        endpoint = reverse('orders')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.post(endpoint, test_order, format='json')
        # print("Response:", json.dumps(response.data, indent=2))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_order_by_id_success(self):
        """Test fetching an order by valid order ID."""
        endpoint = reverse('order-details', kwargs={"order_id": 1})
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.get(endpoint, format='json')
        # print("Response:", json.dumps(response.data, indent=2))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_order_by_invalid_id(self):
        """Test fetching an order by invalid order ID."""
        endpoint = reverse('order-details', kwargs={"order_id": 9999})
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.get(endpoint, format='json')
        # print("Response:", json.dumps(response.data, indent=2))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_all_orders_success(self):
        """Test fetching all orders."""
        endpoint = reverse('orders')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.get(endpoint, format='json')
        # print("Response:", json.dumps(response.data, indent=2))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_orders_with_query_params(self):
        """Test fetching orders with query parameters."""
        endpoint = f"{reverse('orders')}?{urlencode({'order_number':'OD1234'})}"
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.get(endpoint, format='json')
        # print("Response:", json.dumps(response.data, indent=2))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_orders_with_query_params_customer_code(self):
        """Test fetching orders with query parameters."""
        endpoint = f"{reverse('orders')}?{urlencode({'customer_code':'Test123'})}"
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.get(endpoint, format='json')
        # print("Response:", json.dumps(response.data, indent=2))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_order_success(self):
        """Test updating an order successfully."""
        test_order_update = {
            "price": 150.00,
            "item": "Shirt"
        }
        endpoint = reverse('order-details', kwargs={"order_id": 1})
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.put(endpoint, test_order_update, format='json')
        # print("Response:", json.dumps(response.data, indent=2))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_order_invalid_data(self):
        """Test updating an order with invalid data."""
        test_order_update = {
            "price": -100.00  # Negative amount
        }
        endpoint = reverse('order-details', kwargs={"order_id": 1})
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.put(endpoint, test_order_update, format='json')
        # print("Response:", json.dumps(response.data, indent=2))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_nonexistent_order(self):
        """Test updating an order that does not exist."""
        test_order_update = {
            "total_amount": 150.00
        }
        endpoint = reverse('order-details', kwargs={"order_id": 9999})
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.put(endpoint, test_order_update, format='json')
        # print("Response:", json.dumps(response.data, indent=2))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_order_success(self):
        """Test deleting an order successfully."""
        endpoint = reverse('order-details', kwargs={"order_id": 1})
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.delete(endpoint, format='json')
        # print("Response:", json.dumps(response.data, indent=2))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_nonexistent_order(self):
        """Test deleting an order that does not exist."""
        endpoint = reverse('order-details', kwargs={"order_id": 9999})
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.delete(endpoint, format='json')
        # print("Response:", json.dumps(response.data, indent=2))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
