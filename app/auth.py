from functools import wraps
import jwt
from flask import current_app, jsonify, request, g

def _json_error(code: str, message: str, status: int):
  return jsonify({"error": {"code": code, "message": message}}), status

def _get_bearer_token(req) -> str | None:
  auth = req.headers.get("Authorization", "")
  if not auth:
    return None
  if not auth.lower().startswith("bearer "):
    return None
  token = auth.split(" ", 1)[1].strip()
  return token or None

def _decode_jwt(token: str) -> dict:
  secret = current_app.config.get("JWT_SECRET")
  alg = current_app.config.get("JWT_ALG", "HS256")
  return jwt.decode(token, secret, algorithms=[alg], options={"verify_aud": False})

def login_required(fn):
  @wraps(fn)
  def wrapper(*args, **kwargs):
    token = _get_bearer_token(request)
    if not token:
      return _json_error("UNAUTHORIZED", "Missing Bearer token", 401)

    try:
      claims = _decode_jwt(token)
    except jwt.ExpiredSignatureError:
      return _json_error("UNAUTHORIZED", "Token expired", 401)
    except jwt.InvalidTokenError:
      return _json_error("UNAUTHORIZED", "Invalid token", 401)

    user_id = claims.get("sub") or claims.get("id")
    if user_id is None:
      return _json_error("UNAUTHORIZED", "Token missing sub/id", 401)

    # type = role (user/admin/super)
    role = (claims.get("type") or "").strip().lower()

    # status = unverified/active/banned
    status = (claims.get("status") or "").strip().lower()
    if status not in {"unverified", "active", "banned"}:
      # If unknown, treat as unauthorized to be safe
      return _json_error("UNAUTHORIZED", "Invalid status claim", 401)

    if status == "banned":
      return _json_error("FORBIDDEN", "User is banned", 403)

    # Normalize for controllers
    g.user = {
      "userId": str(user_id),
      "role": role,                 # user/admin/super
      "status": status,             # unverified/active
      "verified": status != "unverified",
      **claims,
    }

    return fn(*args, **kwargs)
  return wrapper
