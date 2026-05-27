from pydantic import BaseModel, Field


class AuthUserResponse(BaseModel):
    id: int
    username: str
    role: str


class AuthRegisterRequest(BaseModel):
    username: str = Field(min_length=3, max_length=128)
    password: str = Field(min_length=8, max_length=256)


class AuthLoginRequest(BaseModel):
    username: str = Field(min_length=1, max_length=128)
    password: str = Field(min_length=1, max_length=256)


class AuthTokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in_seconds: int
    user: AuthUserResponse


class AuthRefreshRequest(BaseModel):
    refresh_token: str = Field(min_length=32)


class AuthLogoutRequest(BaseModel):
    refresh_token: str = Field(min_length=32)


class AuthMessageResponse(BaseModel):
    status: str
