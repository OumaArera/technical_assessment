# from django.conf import settings
from myproject import settings
import requests # type: ignore


def validate_token(token):
    try:
        response = requests.get(
            f"https://{settings.AUTH0_DOMAIN}/userinfo",
            headers={"Authorization": f"Bearer {token}"},
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException:
        return None
