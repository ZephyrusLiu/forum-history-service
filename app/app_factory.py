from flask import Flask, g, request
import jwt
from werkzeug.exceptions import HTTPException
from .config import Config
from .db import db
from .message import RErrorMessage
from .routes.health import health_bp
from .routes.history import history_bp

def create_app():
  app = Flask(__name__)
  app.config.from_object(Config)

  try:
    db.init_app(app)
    with app.app_context():
      db.create_all()
  except Exception:
    app.logger.exception("DB init_app/create_all failed")

  app.register_blueprint(health_bp)
  app.register_blueprint(history_bp, url_prefix="/history")

  @app.before_request
  def attach_user_context():
    if request.path == "/health":
      return None

    if not request.path.startswith("/history"):
      return None

    auth = request.headers.get("Authorization", "")
    if not auth or not auth.lower().startswith("bearer "):
      return RErrorMessage(error_text="Missing Bearer token", response_code=401).get()

    token = auth.split(" ", 1)[1].strip()
    if not token:
      return RErrorMessage(error_text="Missing Bearer token", response_code=401).get()

    try:
      claims = jwt.decode(
        token,
        app.config.get("JWT_SECRET"),
        algorithms=[app.config.get("JWT_ALG", "HS256")],
        options={"verify_aud": False},
      )
    except jwt.ExpiredSignatureError:
      return RErrorMessage(error_text="Token expired", response_code=401).get()
    except jwt.InvalidTokenError:
      return RErrorMessage(error_text="Invalid token", response_code=401).get()

    user_id = claims.get("sub") or claims.get("id")
    if user_id is None:
      return RErrorMessage(error_text="Token missing sub/id", response_code=401).get()

    status = (claims.get("status") or "").strip().lower()
    if status == "banned":
      return RErrorMessage(error_text="User is banned", response_code=403).get()

    g.user = {
      "userId": str(user_id),
      "role": (claims.get("type") or "").strip().lower(),
      "status": status,
      "verified": status == "active",
      **claims,
    }

    return None

  @app.errorhandler(HTTPException)
  def handle_http_exception(err):
    description = err.description or "Request failed"
    status_code = err.code or 500
    response = RErrorMessage(error_text=description, response_code=status_code)
    response.add("code", status_code)
    return response.get()

  @app.errorhandler(Exception)
  def handle_unexpected_error(err):
    app.logger.exception("Unhandled exception")
    status_code = 500
    response = RErrorMessage(error_text="Unexpected server error", response_code=status_code)
    response.add("code", status_code)
    response.add("type", type(err).__name__)
    return response.get()

  return app
