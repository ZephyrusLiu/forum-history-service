from flask import Flask
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

  @app.errorhandler(HTTPException)
  def handle_http_exception(err):
    description = err.description or "Request failed"
    response = RErrorMessage(error_text=description, response_code=err.code or 500)
    response.add("code", code)
    return response.get()

  @app.errorhandler(Exception)
  def handle_unexpected_error(err):
    app.logger.exception("Unhandled exception")
    response = RErrorMessage(error_text="Unexpected server error", response_code=500)
    response.add("code", "INTERNAL_SERVER_ERROR")
    response.add("type", type(err).__name__)
    return response.get()

  return app
