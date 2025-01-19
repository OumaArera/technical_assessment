from customers.repositories.users_repo import UserRepository
from orders.utils import generate_unique_order_number
from orders.repositories.orders_repo import OrderRepository


class OrderService:
    """Handles the business logic for orders."""

    @staticmethod
    def create_order(order_data):
        """
        Creates an order in the database.
        """
        try:
            order_data['order_number']= generate_unique_order_number()
            order_data['customer'] = UserRepository.get_user_by_customer_code(
                customer_code=order_data.pop("customer_code")
            )
            new_order = OrderRepository.create_order(order_data=order_data)
            return new_order
        except Exception as ex:
            raise ex

    @staticmethod
    def get_all_orders(query_params):
        """
        Fetches and returns all orders, optionally filtered by query parameters.
        """
        try:
            orders = OrderRepository.get_all_orders()

            if "order_number" in query_params:
                orders = orders.filter(order_number=query_params["order_number"])

            if "customer_code" in query_params:
                orders = orders.filter(customer__customer_code=query_params["customer_code"])
            
            return orders
        except Exception as ex:
            raise ex

    @staticmethod
    def get_order_by_id(order_id):
        """
        Fetches details of an order by ID.
        """
        try:
            return OrderRepository.get_order_by_id(order_id=order_id)
        except Exception as ex:
            raise ex

    @staticmethod
    def update_order(order_id, order_data):
        """
        Updates the details of an existing order.
        """
        try:
            updated_order = OrderRepository.update_order(order_id=order_id, order_data=order_data)
            return updated_order
        except Exception as ex:
            raise ex

    @staticmethod
    def delete_order(order_id):
        """
        Deletes an order by ID.
        """
        try:
            return OrderRepository.delete_order(order_id=order_id)
        except Exception as ex:
            raise ex
