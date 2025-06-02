import datetime
from functools import wraps
from typing import Callable, Any, Optional
import jwt
from flask import request, jsonify
from app.config.settings import Settings

class Token:

    def __init__(self, config: Settings):
        self.config = config

    def create_token(self, username: str) -> str:
        """Gera um token JWT válido."""
        payload = {
            "username": username,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(
                seconds=self.config.JWT_EXP_DELTA_SECONDS
            )
        }
        return jwt.encode(
            payload,
            self.config.JWT_SECRET_KEY,
            algorithm=self.config.JWT_ALGORITHM
        )

    def token_required(self, f: Callable) -> Callable:
        """Decorator para rotas protegidas por JWT."""
        @wraps(f)
        def decorated(*args: Any, **kwargs: Any) -> Any:
            token = self._extract_token()
            if not token:
                return jsonify({"error": "Token is missing!"}), 401
            try:
                self._validate_token(token)
            except jwt.ExpiredSignatureError:
                return jsonify({"error": "Token expired!"}), 401
            except jwt.InvalidTokenError as e:
                return jsonify({"error": f"Invalid token: {str(e)}"}), 401
            return f(*args, **kwargs)
        return decorated

    def _extract_token(self) -> Optional[str]:
        """Extrai o token do cabeçalho Authorization."""
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith(self.config.BEARER_PREFIX):
            return auth_header[len(self.config.BEARER_PREFIX):]
        return None

    def _validate_token(self, token: str) -> dict:
        """Valida o token e retorna o payload."""
        payload = jwt.decode(
            token,
            self.config.JWT_SECRET_KEY,
            algorithms=[self.config.JWT_ALGORITHM]
        )
        if not payload.get("username"):
            raise jwt.InvalidTokenError("Missing username in payload")
        return payload