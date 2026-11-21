from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from backend.app.core.security import verify_token

bearer_scheme = HTTPBearer()

def require_admin(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    username = verify_token(credentials.credentials)

    if not username:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"}
        )

    return username
