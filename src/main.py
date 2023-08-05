from fastapi import FastAPI, Depends

from auth.config import auth_backend, fastapi_users
from auth.models import User
from auth.schemas import UserRead, UserCreate

app = FastAPI(title="Heatsink Test")

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

current_user = fastapi_users.current_user()


@app.get('/protected-route')
def protected_route(user: User = Depends(current_user)):
    return f'hello, {user.email}'

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


# @app.get("/users/{user_id}", response_model=UserRead)
# def read_user(user_id: int, db: Session = Depends(get_db)):
#     db_user = crud.get_user(db, user_id=user_id)
#     if db_user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     return db_user