from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles
from auth.auth_config import auth_backend, fastapi_users
from auth.models import User
from auth.schemas import UserRead, UserCreate
from measurements.router import router as router_measurements
from pages.router import router as router_pages

app = FastAPI(title="Heatsink Test")

app.mount('/static', StaticFiles(directory='static'), name='static')

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(router_measurements)
app.include_router(router_pages)

current_user = fastapi_users.current_user()


# app.include_router(
#     fastapi_users.get_verify_router(UserRead),
#     prefix="/auth",
#     tags=["auth"],
# )
#
# app.include_router(
#     fastapi_users.get_reset_password_router(),
#     prefix="/auth",
#     tags=["auth"],
# )
