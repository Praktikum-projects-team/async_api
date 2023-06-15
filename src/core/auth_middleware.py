from http import HTTPStatus

from fastapi import Request
from fastapi import Header, HTTPException

from typing import Annotated
from starlette.middleware.base import BaseHTTPMiddleware
from httpx import AsyncClient

from src.core.config import AuthConfig


async def get_token_header(x_token: Annotated[str, Header()]):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")


class AuthMiddleware(BaseHTTPMiddleware):
    def __init__(
            self,
            app,
            some_attribute: str,
    ):
        super().__init__(app)
        self.some_attribute = some_attribute
        self.auth_header_key = 'Authorization'
        self.token_type = 'Bearer'

    async def check_token(self, token):
        if not token.startswith(self.token_type):
            return ...

        try:
            user = await self.check_token_with_auth_service(token)
        except Exception:  # todo connection exception
            get_user_info_from_jwt(token)



    async def check_token_with_auth_service(self, token):
        url = AuthConfig().host + '/api/v1/auth/check_access_token'
        async with AsyncClient() as client:
            auth_answer = await client.post(url, headers={self.auth_header_key: token})
        if auth_answer.status_code == 200:
            return auth_answer.json()
        if auth_answer.status_code == HTTPStatus.UNAUTHORIZED:
            return ...


    async def dispatch(self, request: Request, call_next):
        if request.url.path.startswith('/api/v1'):
            auth_header = request.headers.get(self.auth_header_key, '')
            user_info = await self.check_token(auth_header)
            if 'user' not in user_info['roles']:
                return 403

        response = await call_next(request)
        return response
