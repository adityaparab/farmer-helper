from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from farmer_helper.core.config import get_settings
from farmer_helper.db.base import get_db_session
from farmer_helper.db.models.foundation import UserAccount
from farmer_helper.repositories.user_repository import UserRepository
from farmer_helper.services.auth.tokens import decode_access_token

bearer_scheme = HTTPBearer(auto_error=False)
bearer_dependency = Depends(bearer_scheme)
db_session_dependency = Depends(get_db_session)


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = bearer_dependency,
    db: Session = db_session_dependency,
) -> UserAccount:
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
            headers={"WWW-Authenticate": "Bearer"},
        )

    settings = get_settings()
    try:
        claims = decode_access_token(credentials.credentials, secret=settings.auth_jwt_secret)
        user_id = int(claims.subject)
    except (TypeError, ValueError) as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc

    user = UserRepository(db).get_by_id(user_id)
    if user is None or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or inactive user",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


current_user_dependency = Depends(get_current_user)


def require_admin_user(current_user: UserAccount = current_user_dependency) -> UserAccount:
    if current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin role required")
    return current_user


def require_authenticated_user(
    current_user: UserAccount = current_user_dependency,
) -> UserAccount:
    return current_user
