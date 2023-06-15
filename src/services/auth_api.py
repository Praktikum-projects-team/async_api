from http import HTTPStatus

from fastapi import Request
from fastapi import Header, HTTPException

from typing import Annotated
from starlette.middleware.base import BaseHTTPMiddleware
from httpx import AsyncClient

from core.config import AuthConfig


class AuthApi:
    def __init__(self):
        self.auth_header_key = 'Authorization'
        self.token_type = 'Bearer'
        self.token_checking_url = AuthConfig().host + '/api/v1/auth/check_access_token'

    async def check_token(self, token):
        async with AsyncClient() as client:
            auth_answer = await client.post(
                self.token_checking_url,
                headers={self.auth_header_key: self.token_type + ' ' + token}
            )
        if auth_answer.status_code == 200:
            return auth_answer.json()
        if auth_answer.status_code == HTTPStatus.UNAUTHORIZED:
            raise HTTPException(status_code=401, detail="Invalid token or expired token.")


def get_auth_api():
    return AuthApi()
