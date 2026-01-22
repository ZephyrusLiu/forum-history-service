import os

class Config:
  # DB (History DB)
  DB_HOST = os.getenv("DB_HOST", "localhost")
  DB_PORT = os.getenv("DB_PORT", "3306")
  DB_USER = os.getenv("DB_USER", "history_user")
  DB_PASSWORD = os.getenv("DB_PASSWORD", "")
  DB_NAME = os.getenv("DB_NAME", "history_db")

  SQLALCHEMY_DATABASE_URI = (
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
  )
  SQLALCHEMY_TRACK_MODIFICATIONS = False

  # JWT (must match the secret used by User/Auth service)
  JWT_SECRET = os.getenv("JWT_SECRET", "change_me")
  JWT_ALG = os.getenv("JWT_ALG", "HS256")
