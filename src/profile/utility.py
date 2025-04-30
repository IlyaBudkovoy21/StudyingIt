from typing import Optional

from rest_framework_simplejwt.authentication import JWTAuthentication


def get_user_id_by_access(access_token: str) -> Optional[str]:
    jwt_auth = JWTAuthentication()
    try:
        validated_token = jwt_auth.get_validated_token(access_token)
        user = jwt_auth.get_user(validated_token)
        return str(user.id)
    except Exception as e:
        return None
