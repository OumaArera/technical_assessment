import phonenumbers
import re
from rest_framework import serializers
from customers.models.user import User

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'phone_number',
            'first_name',
            'last_name',
            'email',
            'customer_code',
            'created_at',
            'modified_at',
        ]


class UpdateUserDeserializer(serializers.Serializer):
    password = serializers.CharField(required=False, write_only=True)
    phone_number = serializers.CharField(required=False)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)

    def validate_phone_number(self, value):
        """
        Validate that the phone number is valid and in an international format.
        """
        try:
            parsed_number = phonenumbers.parse(value, None)
            if not phonenumbers.is_valid_number(parsed_number):
                raise serializers.ValidationError("Invalid phone number.")
        except phonenumbers.NumberParseException:
            raise serializers.ValidationError("Invalid phone number format.")
        return value


class CustomerDeserializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)
    phone_number = serializers.CharField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    email = serializers.EmailField(required=False)

    def validate_password(self, value):
        """
        Validate that the password is:
        - At least 8 characters long
        - Contains at least one uppercase letter
        - Contains at least one lowercase letter
        - Contains at least one number
        """
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        if not re.search(r"[A-Z]", value):
            raise serializers.ValidationError("Password must contain at least one uppercase letter.")
        if not re.search(r"[a-z]", value):
            raise serializers.ValidationError("Password must contain at least one lowercase letter.")
        if not re.search(r"\d", value):
            raise serializers.ValidationError("Password must contain at least one number.")
        return value

    def validate_phone_number(self, value):
        """
        Validate that the phone number is valid and in an international format.
        """
        try:
            parsed_number = phonenumbers.parse(value, None)
            if not phonenumbers.is_valid_number(parsed_number):
                raise serializers.ValidationError("Invalid phone number.")
        except phonenumbers.NumberParseException:
            raise serializers.ValidationError("Invalid phone number format.")
        return value


class LoginDeserializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)
