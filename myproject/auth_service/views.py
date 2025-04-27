from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from auth_service.token_utils import validate_token

class SignupView(APIView):
    def post(self, request):
        token = request.headers.get("Authorization", "").split(" ")[1]
        user_info = validate_token(token)

        if not user_info:
            return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)

        user, created = User.objects.get_or_create(username=user_info["email"], email=user_info["email"])
        if created:
            return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
        return Response({"message": "User already exists"}, status=status.HTTP_200_OK)


class LoginView(APIView):
    def post(self, request):
        token = request.headers.get("Authorization", "").split(" ")[1]
        user_info = validate_token(token)

        if not user_info:
            return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": "User logged in successfully", "user": user_info}, status=status.HTTP_200_OK)


class LogoutView(APIView):
    def post(self, request):
        request.session.flush()
        return Response({"message": "User logged out successfully"}, status=status.HTTP_204_NO_CONTENT)
