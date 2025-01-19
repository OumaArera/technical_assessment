from rest_framework.authentication import BaseAuthentication # type: ignore
from rest_framework.exceptions import AuthenticationFailed

from myproject.tokens_utils import decode_jwt_token
from customers.models.user import User

from rest_framework.exceptions import APIException

from rest_framework import status



class CustomUnAuthorizedException(APIException):
  """
  Custom exception to return 401 Unauthorized.
  """
  status_code = status.HTTP_401_UNAUTHORIZED
  default_detail = "Authentication token is missing or invalid."
  default_code = "unauthorized"
  

class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        """
        Authenticate the request by validating the JWT token provided in the 'Authorization' header.
        """
        # Retrieve the token from the Authorization header
        auth_header = request.headers.get('Authorization')
        
        if not auth_header:
            raise CustomUnAuthorizedException("You are not authenticated. Please login and try again!")

        token = auth_header.split(" ")[1] if auth_header.startswith('Bearer') else None
        
        if not token:
            raise CustomUnAuthorizedException("You are not authenticated. Please login and try again!")

        # Decode the token
        payload = decode_jwt_token(token=token)

        # Retrieve the user from the payload
        user = self.get_user(user_id=payload.get('user_id'))

        # Return the user and token
        return (user, token)  # Return a tuple of (user, auth)
    
    @staticmethod
    def get_user(user_id):
        """
        Fetch the user from the database using the user_id from the decoded payload.
        """
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise AuthenticationFailed("User not found")

