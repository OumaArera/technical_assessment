# from authlib.integrations.requests_client import OAuth2Session # type: ignore
from django.conf import settings

# def get_auth0_client():
#     return OAuth2Session(
#         client_id=settings.AUTH0_CLIENT_ID,
#         client_secret=settings.AUTH0_SECRET_KEY,
#         scope="openid profile email",
#     )


from jose import jwt
import requests
from django.contrib.auth.models import User

class Auth0Backend:
    def authenticate(self, request, token=None):
        if not token:
            return None

        # Decode the token
        payload = jwt.decode(
            token,
            options={"verify_signature": False},
            audience=f"https://{settings.AUTH0_DOMAIN}/userinfo",
        )
        email = payload.get("email")

        if email:
            user, _ = User.objects.get_or_create(username=email, email=email)
            return user
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
