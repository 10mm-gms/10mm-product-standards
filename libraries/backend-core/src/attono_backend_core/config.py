from pydantic_settings import BaseSettings


class GmsBackendSettings(BaseSettings):
    environment: str = "production"
    log_level: str = "INFO"
    database_url: str
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60
    refresh_token_expire_days: int = 7
    allowed_domain: str
    google_client_id: str | None = None
    google_client_secret: str | None = None
    google_scopes: list[str] = [
        "openid",
        "https://www.googleapis.com/auth/userinfo.email",
        "https://www.googleapis.com/auth/userinfo.profile",
    ]
    ses_region: str | None = None
    ses_access_key: str | None = None
    ses_secret_key: str | None = None
    ses_from_email: str | None = None
    google_chat_webhook_url: str | None = None

    class Config:
        env_file = ".env"
        extra = "allow"
