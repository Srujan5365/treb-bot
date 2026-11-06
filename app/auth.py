import secrets
from fastapi import Depends, HTTPException, Security, status
from fastapi.security import APIKeyHeader, HTTPBasic, HTTPBasicCredentials
from app.config import settings

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)
security_basic = HTTPBasic(auto_error=False)


def authenticate(
    api_key: str = Security(api_key_header),
    credentials: HTTPBasicCredentials = Depends(security_basic),
) -> str:
    """
    Accepts either a valid X-API-Key header OR HTTP Basic Auth.
    Uses constant-time comparison (secrets.compare_digest) to prevent timing attacks.
    """
    if api_key and secrets.compare_digest(api_key, settings.API_KEY):
        return "api-key-client"

    if credentials:
        correct_user = secrets.compare_digest(credentials.username, settings.BASIC_AUTH_USERNAME)
        correct_pass = secrets.compare_digest(credentials.password, settings.BASIC_AUTH_PASSWORD)
        if correct_user and correct_pass:
            return credentials.username

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication credentials",
        headers={"WWW-Authenticate": "Basic"},
    )
