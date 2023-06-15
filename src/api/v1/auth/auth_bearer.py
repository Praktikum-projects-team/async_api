from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt

from src.core.config import AuthConfig

auth_config = AuthConfig()


class BaseJWTBearer(HTTPBearer):
    """
    base class for jwt token checking
    """
    def __init__(self, auto_error: bool = True):
        super(BaseJWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(BaseJWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=403, detail="Invalid token or expired token.")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    def decode_jwt(self, token: str) -> dict:
        try:
            return jwt.decode(token, auth_config.jwt_secret, algorithms=[auth_config.jwt_algorithm])
        except jwt.PyJWTError:
            return {}

    def check_payload(self, jwt_payload):
        """"
        To be overriden if you expect to get certain values from jwt claims(roles, for example)
        """
        return True

    def verify_jwt(self, jwtoken: str) -> bool:

        try:
            payload = self.decode_jwt(jwtoken)
        except:
            payload = None

        return self.check_payload(payload) if payload else False
