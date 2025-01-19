from datetime import timedelta
from django.utils import timezone
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed

import jwt


def generate_jwt_token(user):
	"""
	Generate a JWT access token for the given user.
	"""
	payload = {
		"user_id": user.id,
		"username": user.username,
		"full_name": f"{user.first_name} {user.last_name}",
		"iss": settings.JWT_ISSUER,
		"aud": settings.JWT_AUDIENCE,
		"exp": timezone.now() + timedelta(minutes=30),
		"iat": timezone.now(),
	}
	token = jwt.encode(
		payload=payload,
		key=settings.SECRET_KEY,
		algorithm=settings.JWT_ALGORITHM
	)
	return token


def decode_jwt_token(token: str):
	"""
	Decodes a JWT token and returns the payload.
	"""
	try:
		payload = jwt.decode(
			jwt=token,
			key=settings.SECRET_KEY,
			algorithms=settings.JWT_ALGORITHM,
			audience=settings.JWT_AUDIENCE,
			issuer=settings.JWT_ISSUER
		)
		return payload
	except jwt.ExpiredSignatureError:
		raise AuthenticationFailed("Token has expired")
	except jwt.InvalidTokenError:
		raise AuthenticationFailed("Invalid token")