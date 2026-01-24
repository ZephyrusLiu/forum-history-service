from flask import Blueprint, jsonify
from sqlalchemy import text
from ..db import db
from ..message import RErrorMessage

health_bp = Blueprint("health", __name__)

@health_bp.get("/health")
def health():
  try:
    db.session.execute(text("SELECT 1"))
    return jsonify({"status": "ok", "db": "ok"}), 200
  except Exception as e:
    try:
      db.session.rollback()
    except Exception:
      pass

    response = RErrorMessage(error_text="db connection failed", response_code=503)
    response.add("code", "DB_ERROR")
    response.add("type", type(e).__name__)
    response.add("status", "error")
    response.add("db", "error")
    return response.get()
