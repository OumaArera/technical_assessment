from customers.repositories.users_repo import UserRepository
from customers.utils import generate_unique_customer_code



class UserService:
    """Handles the business logic for users."""

    @staticmethod
    def create_user(user_data):
        """
        Creates a new user in the database.
        """
        try:
            user_data['customer_code'] = generate_unique_customer_code()
            new_user = UserRepository.create_user(user_data=user_data)
            return new_user
        except Exception as ex:
            raise ex

    @staticmethod
    def get_all_users(query_params):
        """
        Fetches and returns all users, optionally filtered by query parameters.
        """
        try:
            users = UserRepository.get_all_users()

            if "email" in query_params:
                users = users.filter(email=query_params["email"])
            if "customer_code" in query_params:
                users = users.filter(customer_code=query_params["customer_code"])

            return users
        except Exception as ex:
            raise ex

    @staticmethod
    def get_user_by_id(user_id):
        """
        Fetches details of a user by ID.
        """
        try:
            return UserRepository.get_user_by_id(user_id=user_id)
        except Exception as ex:
            raise ex

    @staticmethod
    def update_user(user_id, user_data):
        """
        Updates the details of an existing user.
        """
        try:
            updated_user = UserRepository.update_user(user_id=user_id, user_data=user_data)
            return updated_user
        except Exception as ex:
            raise ex

    @staticmethod
    def delete_user(user_id):
        """
        Deletes a user by ID.
        """
        try:
            return UserRepository.delete_user(user_id=user_id)
        except Exception as ex:
            raise ex
