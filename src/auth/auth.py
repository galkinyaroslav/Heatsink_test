from fastapi_users.authentication import CookieTransport, AuthenticationBackend
from fastapi_users.authentication import JWTStrategy
from config import SECRET_KEY_PRIVATE, SECRET_KEY_PUBLIC

cookie_transport = CookieTransport(cookie_name='heatsink_test_cookie', cookie_max_age=3600)

# PRIVATE_KEY = f"""-----BEGIN RSA PRIVATE KEY-----
# {SECRET_KEY_PRIVATE}
# -----END RSA PRIVATE KEY-----"""

# PUBLIC_KEY = f"""-----BEGIN PUBLIC KEY-----
# {SECRET_KEY_PUBLIC}
# # -----END PUBLIC KEY-----"""


# def get_jwt_strategy() -> JWTStrategy:
#     return JWTStrategy(
#         secret=PRIVATE_KEY,
#         lifetime_seconds=3600,
#         algorithm="RS256",
#         public_key=PUBLIC_KEY,
#     )

SECRET = SECRET_KEY_PRIVATE


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)
