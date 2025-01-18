import logging
from django.db import IntegrityError, DatabaseError  # type: ignore
from django.core.exceptions import ValidationError, ObjectDoesNotExist  # type: ignore
from myproject.db_exceptions import (
    NotFoundException,
    IntegrityException,
    QueryException,
    DataBaseException,
)
from customers.models.user import User

logger = logging.getLogger(__name__)

class UserRepository:
    """Handles data layer operations for the User model."""

    @staticmethod
    def create_user(user_data):
        """Creates a new user in the database."""
        try:
            new_user = User.create_user(user_data)
            new_user.full_clean()
            new_user.save()
            return new_user
        except ValidationError as ex:
            logger.error(f"Validation error while creating user: {ex}", exc_info=True)
            raise IntegrityException(message=ex)
        except DatabaseError as ex:
            logger.error(f"Database error while creating user: {ex}", exc_info=True)
            raise QueryException(message="Error executing query to create user.")
        except Exception as ex:
            logger.error(f"Unexpected error while creating user: {ex}", exc_info=True)
            raise DataBaseException("An unexpected error occurred while creating the user.")

    @staticmethod
    def get_all_users():
        """Fetches and returns all users."""
        try:
            users = User.objects.all()
            return users
        except DatabaseError as ex:
            logger.error(f"Database error while fetching users: {ex}", exc_info=True)
            raise QueryException(message="Error executing query to fetch users.")
        except Exception as ex:
            logger.error(f"Unexpected error while fetching users: {ex}", exc_info=True)
            raise DataBaseException("An unexpected error occurred while fetching users.")

    @staticmethod
    def get_user_by_id(user_id):
        """Fetches details of a user by their ID."""
        try:
            user = User.objects.get(pk=user_id)
            return user
        except ObjectDoesNotExist:
            raise NotFoundException(entity_name=f"User with ID {user_id}")
        except DatabaseError as ex:
            logger.error(f"Database error while fetching user by ID: {ex}", exc_info=True)
            raise QueryException(message="Error executing query to fetch user by ID.")
        except Exception as ex:
            logger.error(f"Unexpected error while fetching user by ID: {ex}", exc_info=True)
            raise DataBaseException("An unexpected error occurred while fetching user by ID.")

    @staticmethod
    def update_user(user_id, user_data):
        """Updates details of an existing user."""
        try:
            user = UserRepository.get_user_by_id(user_id)
            for field, value in user_data.items():
                setattr(user, field, value)
            user.full_clean()
            user.save()
            return user
        except ValidationError as ex:
            logger.error(f"Validation error while updating user: {ex}", exc_info=True)
            raise IntegrityException(message=ex)
        except DatabaseError as ex:
            logger.error(f"Database error while updating user: {ex}", exc_info=True)
            raise QueryException(message="Error executing query to update user.")
        except Exception as ex:
            logger.error(f"Unexpected error while updating user: {ex}", exc_info=True)
            raise DataBaseException("An unexpected error occurred while updating the user.")

    @staticmethod
    def delete_user(user_id):
        """Deletes a user record by their ID."""
        try:
            user = UserRepository.get_user_by_id(user_id)
            user.delete()
            return True
        except NotFoundException as ex:
            raise ex
        except IntegrityError as ex:
            logger.error(f"Integrity error while deleting user: {ex}", exc_info=True)
            raise IntegrityException(message=ex)
        except DatabaseError as ex:
            logger.error(f"Database error while deleting user: {ex}", exc_info=True)
            raise QueryException(message="Error executing query to delete user.")
        except Exception as ex:
            logger.error(f"Unexpected error while deleting user: {ex}", exc_info=True)
            raise DataBaseException("An unexpected error occurred while deleting the user.")