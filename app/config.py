import os

class Config:
  DB_HOST = os.getenv("DB_HOST", "localhost")
  DB_PORT = os.getenv("DB_PORT", "3306")
  DB_USER = os.getenv("DB_USER", "history_user")
  DB_PASSWORD = os.getenv("DB_PASSWORD", "change_me")
  DB_NAME = os.getenv("DB_NAME", "history_db")

  SQLALCHEMY_DATABASE_URI = (
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
  )
  SQLALCHEMY_TRACK_MODIFICATIONS = False
