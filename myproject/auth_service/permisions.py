from rest_framework.permissions import BasePermission
from jose import jwt # type: ignore
from django.conf import settings

class IsAuthenticatedWithAuth0(BasePermission):
    def has_permission(self, request, view):
        auth_header = request.headers.get("Authorization", None)
        if not auth_header:
            return False

        token = auth_header.split()[1]  # "Bearer <token>"
        try:
            payload = jwt.decode(
                token,
                settings.AUTH0_CLIENT_SECRET,
                algorithms=["RS256"],
                audience=settings.AUTH0_API_AUDIENCE,
                issuer=f"https://{settings.AUTH0_DOMAIN}/",
            )
            request.user = payload  # Attach user info to the request
            return True
        except jwt.ExpiredSignatureError:
            return False
        except jwt.JWTClaimsError:
            return False
        except Exception:
            return False
