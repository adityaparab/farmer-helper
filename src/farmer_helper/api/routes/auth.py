from datetime import UTC, datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from farmer_helper.core.config import get_settings
from farmer_helper.db.base import get_db_session
from farmer_helper.db.models.foundation import UserAccount
from farmer_helper.repositories.user_repository import RefreshTokenRepository, UserRepository
from farmer_helper.schemas.auth import (
    AuthLoginRequest,
    AuthLogoutRequest,
    AuthMessageResponse,
    AuthRefreshRequest,
    AuthRegisterRequest,
    AuthTokenResponse,
    AuthUserResponse,
)
from farmer_helper.services.auth.dependencies import get_current_user
from farmer_helper.services.auth.passwords import (
    DEFAULT_ADMIN_PASSWORD_HASH,
    hash_password,
    verify_password,
)
from farmer_helper.services.auth.tokens import (
    create_access_token,
    create_refresh_token,
    hash_refresh_token,
)

router = APIRouter(prefix="/auth", tags=["auth"])


def _to_user_response(user: UserAccount) -> AuthUserResponse:
    return AuthUserResponse(id=user.id, username=user.username, role=user.role)


def ensure_default_admin_user(db: Session) -> UserAccount:
    repo = UserRepository(db)
    existing = repo.get_by_username("admin")
    if existing is not None:
        return existing
    return repo.create_user(
        username="admin",
        password_hash=DEFAULT_ADMIN_PASSWORD_HASH,
        role="admin",
    )


def _issue_tokens(*, db: Session, user: UserAccount) -> AuthTokenResponse:
    settings = get_settings()
    access_ttl_seconds = settings.auth_access_token_ttl_minutes * 60
    access_token = create_access_token(
        user_id=user.id,
        username=user.username,
        role=user.role,
        secret=settings.auth_jwt_secret,
        ttl_seconds=access_ttl_seconds,
    )
    refresh_token = create_refresh_token()
    RefreshTokenRepository(db).create(
        user_id=user.id,
        token_hash=hash_refresh_token(refresh_token),
        expires_at=datetime.now(UTC) + timedelta(days=settings.auth_refresh_token_ttl_days),
    )
    return AuthTokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in_seconds=access_ttl_seconds,
        user=_to_user_response(user),
    )


@router.post("/register", response_model=AuthTokenResponse, status_code=201)
def register_user(
    payload: AuthRegisterRequest,
    db: Session = Depends(get_db_session),
) -> AuthTokenResponse:  # noqa: B008
    ensure_default_admin_user(db)
    repo = UserRepository(db)
    username = payload.username.strip().lower()
    if username == "admin" or repo.get_by_username(username) is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username already exists")

    user = repo.create_user(
        username=username,
        password_hash=hash_password(payload.password),
        role="user",
    )
    return _issue_tokens(db=db, user=user)


@router.post("/login", response_model=AuthTokenResponse)
def login_user(
    payload: AuthLoginRequest,
    db: Session = Depends(get_db_session),
) -> AuthTokenResponse:  # noqa: B008
    ensure_default_admin_user(db)
    user = UserRepository(db).get_by_username(payload.username)
    if (
        user is None
        or not user.is_active
        or not verify_password(payload.password, user.password_hash)
    ):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return _issue_tokens(db=db, user=user)


@router.post("/refresh", response_model=AuthTokenResponse)
def refresh_session(
    payload: AuthRefreshRequest,
    db: Session = Depends(get_db_session),
) -> AuthTokenResponse:  # noqa: B008
    token_hash = hash_refresh_token(payload.refresh_token)
    record = RefreshTokenRepository(db).get_active(
        token_hash=token_hash,
        now=datetime.now(UTC),
    )
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        )

    user = UserRepository(db).get_by_id(record.user_id)
    if user is None or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        )
    return _issue_tokens(db=db, user=user)


@router.post("/logout", response_model=AuthMessageResponse)
def logout_user(
    payload: AuthLogoutRequest,
    db: Session = Depends(get_db_session),
) -> AuthMessageResponse:  # noqa: B008
    RefreshTokenRepository(db).revoke(
        token_hash=hash_refresh_token(payload.refresh_token),
        now=datetime.now(UTC),
    )
    return AuthMessageResponse(status="ok")


@router.get("/me", response_model=AuthUserResponse)
def get_me(current_user: UserAccount = Depends(get_current_user)) -> AuthUserResponse:  # noqa: B008
    return _to_user_response(current_user)
