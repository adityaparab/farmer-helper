from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from farmer_helper.db.models.foundation import RefreshTokenRecord, UserAccount


class UserRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_id(self, user_id: int) -> UserAccount | None:
        return self.db.get(UserAccount, user_id)

    def get_by_username(self, username: str) -> UserAccount | None:
        normalized = username.strip().lower()
        return self.db.scalar(select(UserAccount).where(UserAccount.username == normalized))

    def create_user(self, *, username: str, password_hash: str, role: str = "user") -> UserAccount:
        user = UserAccount(
            username=username.strip().lower(),
            password_hash=password_hash,
            role=role,
            is_active=True,
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user


class RefreshTokenRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, *, user_id: int, token_hash: str, expires_at: datetime) -> RefreshTokenRecord:
        record = RefreshTokenRecord(user_id=user_id, token_hash=token_hash, expires_at=expires_at)
        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)
        return record

    def get_active(self, *, token_hash: str, now: datetime) -> RefreshTokenRecord | None:
        return self.db.scalar(
            select(RefreshTokenRecord).where(
                RefreshTokenRecord.token_hash == token_hash,
                RefreshTokenRecord.revoked_at.is_(None),
                RefreshTokenRecord.expires_at > now,
            )
        )

    def revoke(self, *, token_hash: str, now: datetime) -> bool:
        record = self.db.scalar(
            select(RefreshTokenRecord).where(RefreshTokenRecord.token_hash == token_hash)
        )
        if record is None or record.revoked_at is not None:
            return False
        record.revoked_at = now
        self.db.commit()
        return True
