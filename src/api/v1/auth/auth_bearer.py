import json
import logging

from fastapi import Request, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from httpx import ConnectError
import jwt

from core.config import AuthConfig
from services.auth_api import get_auth_api, AuthApi

auth_config = AuthConfig()


class BaseJWTBearer(HTTPBearer):
    """
    base class for jwt token checking
    """
    def __init__(self, auto_error: bool = True):
        super(BaseJWTBearer, self).__init__(auto_error=auto_error)
        self.token_type = 'Bearer'

    async def __call__(self, request: Request, auth_api: AuthApi = Depends(get_auth_api)):
        credentials: HTTPAuthorizationCredentials = await super(BaseJWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == self.token_type:
                raise HTTPException(status_code=401, detail="Invalid authentication scheme.")
            if not await self.verify_jwt(request.app.state.logger, credentials.credentials, auth_api):
                raise HTTPException(status_code=403, detail="Invalid token or expired token.")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    def decode_jwt(self, token: str) -> dict:
        try:
            payload = jwt.decode(token, auth_config.jwt_secret, algorithms=[auth_config.jwt_algorithm])
            return json.loads(payload.get('user_info'))
        except jwt.PyJWTError:
            return {}

    def check_payload(self, jwt_payload):
        """"
        To be overriden if you expect to get certain values from user info (roles, for example)
        """
        return True

    async def verify_jwt(self, logger:logging.Logger, jwtoken: str, auth_api: AuthApi) -> bool:

        try:
            current_user = await auth_api.check_token(jwtoken)
        except ConnectError:
            logger.exception('auth api connection error')
            current_user = self.decode_jwt(jwtoken)

        return self.check_payload(current_user) if current_user else False
