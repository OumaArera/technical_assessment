from django.db import models # type: ignore
from django.contrib.auth.models import AbstractUser # type: ignore
from django.utils.translation import gettext_lazy as gtl # type: ignore
from phonenumber_field.modelfields import PhoneNumberField # type: ignore


class User(AbstractUser):
    """
    Custom User model that includes additional fields.
    """
    username = models.CharField(
        max_length=255,
        unique=True,
        error_messages={"unique": gtl("A user with that username already exists.")},
    )
    phone_number = PhoneNumberField(
        unique=True,
        error_messages={"unique": gtl("A customer with the provided phone number already exists")},
        help_text=gtl("Enter a valid phone number"),
    )
    password = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(
        null=True,
        blank=True,
        unique=True,
        error_messages={"unique": gtl("A user with that email already exists.")},
    )
    customer_code = models.CharField(
        max_length=100,
        unique=True,
        error_messages={"unique": gtl("A customer with the provided code already exists")},
    )
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    # Override the reverse relationships for groups and user_permissions
    groups = models.ManyToManyField(
        "auth.Group",
        related_name="custom_user_groups",
        blank=True,
        help_text=gtl(
            "The groups this user belongs to. A user will get all permissions granted to each of their groups."
        ),
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="custom_user_permissions",
        blank=True,
        help_text=gtl("Specific permissions for this user."),
    )

    def save(self, *args, **kwargs):
        if self.email == "":
            self.email = None
        super().save(*args, **kwargs)

    @classmethod
    def create_user(cls, validated_data):
        """Creates a new user instance from the validated data."""
        password = validated_data.pop("password")
        user = cls(**validated_data)
        
        user.set_password(password)
        user.full_clean()
        user.save()
        return user
