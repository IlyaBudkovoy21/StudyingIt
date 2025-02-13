from rest_framework_simplejwt.authentication import JWTAuthentication


def get_username_by_access(access_token):
    jwt_auth = JWTAuthentication()
    try:
        validated_token = jwt_auth.get_validated_token(access_token)
        user = jwt_auth.get_user(validated_token)
        return {"status": "OK", "data": str(user.id)}
    except Exception as e:
        return {"status": "ERROR", "error": "Invalid Token"}
