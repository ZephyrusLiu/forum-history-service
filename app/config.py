import os

class Config:
  # DB (History DB)
  DB_HOST = os.getenv("HISTORY_DB_HOST", "localhost")
  DB_PORT = os.getenv("HISTORY_DB_PORT", "3306")
  DB_USER = os.getenv("HISTORY_DB_USER", "history_user")
  DB_PASSWORD = os.getenv("HISTORY_DB_PASSWORD", "")
  DB_NAME = os.getenv("HISTORY_DB_NAME", "history_db")

  SQLALCHEMY_DATABASE_URI = (
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
  )
  SQLALCHEMY_TRACK_MODIFICATIONS = False

  # Post service (for keyword search)
  POST_SERVICE_URL = os.getenv("POST_SERVICE_URL", "http://host.docker.internal:5004")

  # JWT (must match the secret used by User/Auth service)
  JWT_SECRET = os.getenv("JWT_SECRET", "change_me")
  JWT_ALG = os.getenv("JWT_ALG", "HS256")
