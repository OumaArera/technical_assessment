from rest_framework.views import APIView  # type: ignore
from rest_framework.response import Response  # type: ignore
from rest_framework import status  # type: ignore

from customers.services.user_service import UserService
from customers.serializers.model_serializers import CustomerDeserializer, CustomerSerializer, UpdateUserDeserializer
from myproject.validate_params import validate_query_params
from myproject.responses import APIResponse

class UserView(APIView):
    """User view for handling Customer"""

    def post(self, request):
        """Handles creating a new user."""
        # print(f"User: {request.user}")
        try:
            deserializer = CustomerDeserializer(data=request.data)
            if deserializer.is_valid():
                validated_data = deserializer.validated_data
                new_user = UserService.create_user(user_data=validated_data)
                serialized_user = CustomerSerializer(instance=new_user)
                return Response(
                    APIResponse.success(
                        code="00",
                        message="User created successfully",
                        data=serialized_user.data
                    ),
                    status=status.HTTP_201_CREATED
                )
            return Response(
                APIResponse.error(
                    code="99",
                    message="Validation failed",
                    error=deserializer.errors
                ),
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as ex:
            return Response(
                APIResponse.error(
                    code="99",
                    message="An error occurred while creating the user",
                    error=str(ex)
                ),
                status=ex.status_code
            )

    def get(self, request, user_id=None):
        """Handles fetching users."""
        try:
            if user_id:
                user = UserService.get_user_by_id(user_id=user_id)
                serialized_user = CustomerSerializer(instance=user)
                return Response(
                    APIResponse.success(
                        code="00",
                        message="User fetched successfully",
                        data=serialized_user.data
                    ),
                    status=status.HTTP_200_OK
                )
            else:
                query_params = validate_query_params(
                    query_params=request.query_params,
                    valid_query_params={"email", "customer_code"}
                )
                users = UserService.get_all_users(query_params=query_params)
                serialized_users = CustomerSerializer(users, many=True)
                return Response(
                    APIResponse.success(
                        code="00",
                        message="Users fetched successfully",
                        data=serialized_users.data
                    ),
                    status=status.HTTP_200_OK
                )
        except Exception as ex:
            return Response(
                APIResponse.error(
                    code="99",
                    message="Error fetching users",
                    error=str(ex)
                ),
                status=ex.status_code
            )

    def put(self, request, user_id):
        """Handles updating a user."""
        try:
            deserializer = UpdateUserDeserializer(data=request.data)
            if deserializer.is_valid():
                validated_data = deserializer.validated_data
                updated_user = UserService.update_user(user_id=user_id, user_data=validated_data)
                serialized_user = CustomerSerializer(instance=updated_user)
                return Response(
                    APIResponse.success(
                        code="00",
                        message="User updated successfully",
                        data=serialized_user.data
                    ),
                    status=status.HTTP_200_OK
                )
            return Response(
                APIResponse.error(
                    code="99",
                    message="Validation failed",
                    error=deserializer.errors
                ),
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as ex:
            return Response(
                APIResponse.error(
                    code="99",
                    message="Error updating user",
                    error=str(ex)
                ),
                status=ex.status_code
            )

    def delete(self, request, user_id):
        """Handles deleting a user."""
        try:
            if UserService.delete_user(user_id=user_id):
                return Response(
                    APIResponse.success(
                        code="00",
                        message="User deleted successfully",
                        data={"user_id": user_id}
                    ),
                    status=status.HTTP_200_OK
                )
            return Response(
                APIResponse.error(
                    code="99",
                    message="Failed to delete user",
                    error="User not found or already deleted"
                ),
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as ex:
            return Response(
                APIResponse.error(
                    code="99",
                    message="Error deleting user",
                    error=str(ex)
                ),
                status=ex.status_code
            )
