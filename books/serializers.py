from rest_framework import serializers
from .models import Book, AdminUser
from django.contrib.auth import get_user_model

# Get the custom user model (AdminUser) defined in your project
User = get_user_model()

# -------------------------------
# 🔹 Admin User Serializer
# -------------------------------
class AdminUserSerializer(serializers.ModelSerializer):
    """
    Serializer for the AdminUser model.
    Handles conversion between AdminUser instances and JSON,
    and ensures that passwords are hashed when creating a new user.
    """

    class Meta:
        model = User  # Using the custom user model
        fields = ["id", "email", "password"]
        extra_kwargs = {
            "password": {
                "write_only": True,  # Do not include the password in API responses
                "min_length": 6      # Enforce a minimum password length
            },
        }

    def create(self, validated_data):
        """
        Create a new user with a hashed password.
        Steps:
         1. Remove the raw password from the validated data.
         2. Create a new user instance using the remaining data.
         3. Use set_password() to hash the password.
         4. Save and return the new user.
        """
        password = validated_data.pop("password")  # Safely extract the password
        user = User(**validated_data)              # Create user instance with remaining data
        user.set_password(password)                # Hash the password
        user.save()                                # Save the user to the database
        return user


# -------------------------------
# 🔹 Book Serializer
# -------------------------------
class BookSerializer(serializers.ModelSerializer):
    """
    Serializer for the Book model.
    Converts Book model instances to and from JSON.
    """

    class Meta:
        model = Book  # The model to serialize
        fields = "__all__"  # Include all fields from the Book model

    def validate_quantity(self, value):
        """
        Validate that the quantity field is a non-negative integer.
        Raise a validation error if the value is not valid.
        """
        if not isinstance(value, int) or value < 0:
            raise serializers.ValidationError("Quantity must be a non-negative integer.")
        return value
