from flask import Flask
from .config import Config
from .db import db
from .routes.health import health_bp
from .routes.history import history_bp

def create_app():
  app = Flask(__name__)
  app.config.from_object(Config)

  db.init_app(app)

  app.register_blueprint(health_bp)
  app.register_blueprint(history_bp, url_prefix="/history")

  return app
