import logging
from django.db import IntegrityError, DatabaseError  # type: ignore
from django.core.exceptions import ValidationError, ObjectDoesNotExist  # type: ignore
from myproject.db_exceptions import (
    NotFoundException,
    IntegrityException,
    QueryException,
    DataBaseException,
)
from orders.models.orders import Order

logger = logging.getLogger(__name__)

class OrderRepository:
    """Handles data layer operations for the Order model."""

    @staticmethod
    def create_order(order_data):
        """Creates a new order in the database."""
        try:
            new_order = Order.create_order(order_data)
            new_order.full_clean()
            new_order.save()
            return new_order
        except ValidationError as ex:
            logger.error(f"Validation error while creating order: {ex}", exc_info=True)
            raise IntegrityException(message=ex)
        except DatabaseError as ex:
            logger.error(f"Database error while creating order: {ex}", exc_info=True)
            raise QueryException(message="Error executing query to create order.")
        except Exception as ex:
            logger.error(f"Unexpected error while creating order: {ex}", exc_info=True)
            raise DataBaseException("An unexpected error occurred while creating the order.")

    @staticmethod
    def get_all_orders():
        """Fetches and returns all orders."""
        try:
            orders = Order.objects.all()
            return orders
        except DatabaseError as ex:
            logger.error(f"Database error while fetching orders: {ex}", exc_info=True)
            raise QueryException(message="Error executing query to fetch orders.")
        except Exception as ex:
            logger.error(f"Unexpected error while fetching orders: {ex}", exc_info=True)
            raise DataBaseException("An unexpected error occurred while fetching orders.")

    @staticmethod
    def get_order_by_id(order_id):
        """Fetches details of an order by its ID."""
        try:
            order = Order.objects.get(pk=order_id)
            return order
        except ObjectDoesNotExist:
            raise NotFoundException(entity_name=f"Order with ID {order_id}")
        except DatabaseError as ex:
            logger.error(f"Database error while fetching order by ID: {ex}", exc_info=True)
            raise QueryException(message="Error executing query to fetch order by ID.")
        except Exception as ex:
            logger.error(f"Unexpected error while fetching order by ID: {ex}", exc_info=True)
            raise DataBaseException("An unexpected error occurred while fetching order by ID.")

    @staticmethod
    def update_order(order_id, order_data):
        """Updates details of an existing order."""
        try:
            order = OrderRepository.get_order_by_id(order_id)
            for field, value in order_data.items():
                setattr(order, field, value)
            order.full_clean()
            order.save()
            return order
        except NotFoundException as ex:
            raise ex
        except ValidationError as ex:
            logger.error(f"Validation error while updating order: {ex}", exc_info=True)
            raise IntegrityException(message=ex)
        except DatabaseError as ex:
            logger.error(f"Database error while updating order: {ex}", exc_info=True)
            raise QueryException(message="Error executing query to update order.")
        except Exception as ex:
            logger.error(f"Unexpected error while updating order: {ex}", exc_info=True)
            raise DataBaseException("An unexpected error occurred while updating the order.")

    @staticmethod
    def delete_order(order_id):
        """Deletes an order record by its ID."""
        try:
            order = OrderRepository.get_order_by_id(order_id)
            order.delete()
            return True
        except NotFoundException as ex:
            raise ex
        except IntegrityError as ex:
            logger.error(f"Integrity error while deleting order: {ex}", exc_info=True)
            raise IntegrityException(message=ex)
        except DatabaseError as ex:
            logger.error(f"Database error while deleting order: {ex}", exc_info=True)
            raise QueryException(message="Error executing query to delete order.")
        except Exception as ex:
            logger.error(f"Unexpected error while deleting order: {ex}", exc_info=True)
            raise DataBaseException("An unexpected error occurred while deleting the order.")
