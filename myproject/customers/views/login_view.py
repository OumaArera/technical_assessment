from rest_framework import status # type: ignore
from rest_framework.exceptions import AuthenticationFailed # type: ignore
from rest_framework.response import Response # type: ignore
from rest_framework.views import APIView # type: ignore
from django.contrib.auth import authenticate # type: ignore
from rest_framework.permissions import AllowAny # type: ignore

from myproject.tokens_utils import generate_jwt_token
# from cutomers.serializers import LoginSerializer
from customers.serializers.model_serializers import LoginDeserializer
from myproject.responses import APIResponse

class LoginView(APIView):
	"""
	View to authenticate users using their username and password.
	- Generates a JWT access token for authenticated users.
	- Ensures the user's status is active.
	"""
	authentication_classes = []
	permission_classes = [AllowAny]

	def post(self, request):
		"""
		Handles user login.
		"""
		try:
			serializer = LoginDeserializer(data=request.data)
			
			if serializer.is_valid():
				
				username = serializer.validated_data['username']
				password = serializer.validated_data['password']
				
				# Authenticate user using Django's authenticate method
				user = authenticate(username=username, password=password)
				
				if not user:
					raise AuthenticationFailed("Invalid username or password")
				
				if user and not user.is_active:
					raise AuthenticationFailed("User account is inactive. Contact System administrator.", code=400)
				
				# Generate JWT token
				token = generate_jwt_token(user)
				return Response(
					data=APIResponse.success('00', 'User successfully logged in', data={'token':token}),
					status=status.HTTP_200_OK,
					content_type='application/json'
				)
			else:
				return Response(
					data=APIResponse.error('01', "Validation failed", error=serializer.errors),
					status=status.HTTP_400_BAD_REQUEST
				)
		except Exception as ex:
			return Response(
				data=APIResponse.error('03', "An error occurred while logging the user", ex),
				status=ex.status_code if ex.status_code else ex.code
			)