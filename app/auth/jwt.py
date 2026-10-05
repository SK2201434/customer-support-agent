import jwt

from app.config.settings import settings


JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_MINUTES = 60


def create_access_token(
    user_id: str,
    role: str,
) -> str:
    """Create a JWT access token for an authenticated user."""

    payload = {
        "sub": user_id,
        "role": role,
    }

    return jwt.encode(
        payload,
        settings.jwt_secret_key,
        algorithm=JWT_ALGORITHM,
    )


def decode_access_token(token: str) -> dict:
    """Decode and validate a JWT access token."""

    return jwt.decode(
        token,
        settings.jwt_secret_key,
        algorithms=[JWT_ALGORITHM],
    )