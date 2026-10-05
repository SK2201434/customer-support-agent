import uuid

from app.auth.models import AuthenticatedUser
from app.auth.password import hash_password, verify_password
from app.repositories.user import UserRepository
from app.auth.jwt import create_access_token


class AuthenticationService:
    """Service responsible for user registration and authentication."""

    def __init__(self, repository: UserRepository):
        self.repository = repository

    def register_user(
        self,
        email: str,
        password: str,
        role: str = "customer",
    ) -> dict:
        """Register a new user."""

        existing_user = self.repository.get_user_by_email(email)

        if existing_user is not None:
            raise ValueError("A user with this email already exists.")

        user_id = str(uuid.uuid4())
        password_hash = hash_password(password)

        return self.repository.create_user(
            user_id=user_id,
            email=email,
            password_hash=password_hash,
            role=role,
        )

    def authenticate_user(
        self,
        email: str,
        password: str,
    ) -> AuthenticatedUser | None:
        """Authenticate a user using email and password."""

        user = self.repository.get_user_by_email(email)

        if user is None:
            return None

        if not verify_password(
            password,
            user["password_hash"],
        ):
            return None

        return AuthenticatedUser(
            user_id=user["id"],
            role=user["role"],
        )

    def login_user(
        self,
        email: str,
        password: str,
    ) -> str | None:
        """Authenticate a user and return a JWT access token."""

        user = self.authenticate_user(
            email=email,
            password=password,
        )

        if user is None:
            return None

        return create_access_token(
            user_id=user.user_id,
            role=user.role,
        )