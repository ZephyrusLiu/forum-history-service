from flask import Blueprint, jsonify
from sqlalchemy import text
from ..db import db
from ..message import Message

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

    return Message.error(
      "DB_ERROR",
      "db connection failed",
      503,
      error_type=type(e).__name__,
      extra={"status": "error", "db": "error"},
    )
