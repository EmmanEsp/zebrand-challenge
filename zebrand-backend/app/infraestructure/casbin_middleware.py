from typing import Any, Optional
from pathlib import Path

import casbin

from fastapi.responses import JSONResponse
from jose import jwt

from fastapi import Request, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.domain.settings.security_settings import get_security_setting


class CasbinMiddleware:
    def __init__(self, app):
        self.app = app
        self.enforcer = self.setup_casbin()
        self.security = HTTPBearer(auto_error=False)

    def setup_casbin(self):
        """Initialize Casbin enforcer with model and policy files"""
        path = Path(__file__).parent
        
        model_path = str(path / "rbac_model.conf")
        policy_path = str(path / "rbac_policy.csv")

        enforcer = casbin.Enforcer(model_path, policy_path)
        
        return enforcer

    async def get_current_user_role(self, request: Request) -> Optional[dict]:
        """Extract and validate JWT token, return payload with role"""
        credentials: HTTPAuthorizationCredentials = await self.security(request)
        if not credentials:
            return None
            
        security_settings = get_security_setting()
        payload = jwt.decode(
            credentials.credentials,
            security_settings.secret_key,
            algorithms=[security_settings.algorithm]
        )
        return payload

    async def __call__(self, scope: dict, receive: Any, send: Any) -> None:
        if scope["type"] != "http":
            return await self.app(scope, receive, send)
        
        request = Request(scope, receive)

        if request.url.path in ["/docs", "/openapi.json", "/api/v1/auth/sign-in", "/api/v1/auth/guest"]:
            return await self.app(scope, receive, send)

        user_payload = await self.get_current_user_role(request)
        if not user_payload or "role" not in user_payload:
            response = JSONResponse(
                status_code=status.HTTP_403_FORBIDDEN,
                content={
                    "service_status": "fail",
                    "status_code": status.HTTP_403_FORBIDDEN,
                    "data": {"authentication": "Invalid token."}
                }
            )
            await response(scope, receive, send)
            return

        if not self.enforcer.enforce(user_payload["role"], request.url.path, request.method):
            response = JSONResponse(
                status_code=status.HTTP_403_FORBIDDEN,
                content={
                    "service_status": "fail",
                    "status_code": status.HTTP_403_FORBIDDEN,
                    "data": {"authentication": "Invalid role for the action and resource."}
                }
            )
            await response(scope, receive, send)
            return

        await self.app(scope, receive, send)
