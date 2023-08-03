from fastapi_users.authentication import CookieTransport, AuthenticationBackend
from fastapi_users.authentication import JWTStrategy
from config import SECRET_KEY_PRIVATE, SECRET_KEY_PUBLIC, SECRET_KEY_HS256

cookie_transport = CookieTransport(cookie_name='heatsink_test_cookie', cookie_max_age=3600, cookie_secure=False)

PRIVATE_KEY = SECRET_KEY_PRIVATE
PUBLIC_KEY = SECRET_KEY_PUBLIC


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(
        secret=PRIVATE_KEY,
        lifetime_seconds=3600,
        algorithm="RS256",
        public_key=PUBLIC_KEY
    )

# SECRET = SECRET_KEY_HS256
#
#
# def get_jwt_strategy() -> JWTStrategy:
#     return JWTStrategy(secret=SECRET, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)
