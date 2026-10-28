from contextlib import contextmanager
from datetime import datetime, timedelta, timezone
import os
from pathlib import Path
import sqlite3
from typing import Annotated, Iterator

import jwt
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from pydantic import BaseModel, EmailStr, Field
from pwdlib import PasswordHash

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")
password_hash = PasswordHash.recommended()
ACCESS_TOKEN_LIFETIME = timedelta(minutes=30)


class RegistrationRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class UserResponse(BaseModel):
    email: EmailStr


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


def _database_path() -> str:
    return os.getenv("AUTH_DATABASE_PATH", str(Path(__file__).with_name("users.db")))


@contextmanager
def _database_connection() -> Iterator[sqlite3.Connection]:
    connection = sqlite3.connect(_database_path(), timeout=5)
    connection.row_factory = sqlite3.Row
    try:
        with connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    email TEXT PRIMARY KEY,
                    hashed_password TEXT NOT NULL
                )
                """
            )
            yield connection
    finally:
        connection.close()


def _find_user(email: str) -> sqlite3.Row | None:
    with _database_connection() as connection:
        return connection.execute(
            "SELECT email, hashed_password FROM users WHERE email = ?",
            (email,),
        ).fetchone()


def _jwt_secret_key() -> str:
    secret_key = os.getenv("JWT_SECRET_KEY", "")
    if len(secret_key) < 32:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Authentication is not configured",
        )
    return secret_key


def _unauthorized() -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid email or password",
        headers={"WWW-Authenticate": "Bearer"},
    )


@router.post(
    "/auth/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register_user(request: RegistrationRequest) -> UserResponse:
    email = str(request.email).strip().lower()
    hashed_password = password_hash.hash(request.password)
    try:
        with _database_connection() as connection:
            connection.execute(
                "INSERT INTO users (email, hashed_password) VALUES (?, ?)",
                (email, hashed_password),
            )
    except sqlite3.IntegrityError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An account with this email already exists",
        ) from error
    return UserResponse(email=email)


@router.post("/auth/token", response_model=TokenResponse)
def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> TokenResponse:
    email = form_data.username.strip().lower()
    user = _find_user(email)
    if user is None or not password_hash.verify(
        form_data.password,
        user["hashed_password"],
    ):
        raise _unauthorized()

    token = jwt.encode(
        {
            "sub": user["email"],
            "exp": datetime.now(timezone.utc) + ACCESS_TOKEN_LIFETIME,
        },
        _jwt_secret_key(),
        algorithm="HS256",
    )
    return TokenResponse(access_token=token, token_type="bearer")


def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
) -> UserResponse:
    try:
        payload = jwt.decode(token, _jwt_secret_key(), algorithms=["HS256"])
    except InvalidTokenError as error:
        raise _unauthorized() from error

    email = payload.get("sub")
    if not isinstance(email, str):
        raise _unauthorized()

    user = _find_user(email)
    if user is None:
        raise _unauthorized()
    return UserResponse(email=user["email"])


@router.get("/users/me", response_model=UserResponse)
def read_current_user(
    current_user: Annotated[UserResponse, Depends(get_current_user)],
) -> UserResponse:
    return current_user