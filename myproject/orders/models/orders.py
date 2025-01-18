from django.db import models  # type: ignore
from django.utils.translation import gettext_lazy as gtl  # type: ignore
from customers.models.user import User


class Order(models.Model):
    """Order model to store order details"""
    order_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(
        User,  
        on_delete=models.CASCADE, 
        related_name="users",
        help_text=gtl("The customer placing the order")
    )
    item = models.CharField(max_length=100, help_text=gtl("Name of the item ordered"))
    price = models.FloatField(help_text=gtl("Price of the ordered item"))
    order_number = models.CharField(
        max_length=50,
        unique=True,
        error_messages={"unique": gtl("An order with this number already exists")},
        help_text=gtl("Unique order identifier")
    )
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    @classmethod
    def create_order(cls, validated_data):
        """
        Create a new order instance from validated data.
        """
        order = cls(**validated_data)
        return order
