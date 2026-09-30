from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi import Depends, HTTPException, status
from .settings import settings
from typing import Annotated
import secrets

security = HTTPBasic()

def verify_admin(credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
    username_ok = secrets.compare_digest(
        credentials.username.encode("utf-8"), settings.admin_username.encode("utf-8"))
    
    password_ok = secrets.compare_digest(
        credentials.password.encode("utf-8"), settings.admin_password.encode("utf-8"))
    
    if not (username_ok and password_ok):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Wrong password or username!", headers={"WWW-Authenticate": "Basic"})