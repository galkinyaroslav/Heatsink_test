from typing import Optional

from fastapi import Depends, Request, Response
from fastapi_users import BaseUserManager, IntegerIDMixin

from config import SECRET_KEY_RESET, SECRET_KEY_VERIFICATION
from auth.models import User
from auth.utils import get_user_db


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = SECRET_KEY_RESET
    verification_token_secret = SECRET_KEY_VERIFICATION

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        print(f"User {user.username} has registered.")

    async def on_after_forgot_password(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"User {user.username} has forgot their password. Reset token: {token}")

    async def on_after_request_verify(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"Verification requested for user {user.username}. Verification token: {token}")

    async def on_after_login(
            self,
            user: User,
            request: Optional[Request] = None,
            response: Optional[Response] = None,
    ):
        print(f"User {user.username} logged in.")


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)