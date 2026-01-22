from flask import Blueprint, jsonify
from sqlalchemy import text
from ..db import db

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

    return jsonify({
      "status": "error",
      "db": "error",
      "error": {"code": "DB_ERROR", "message": "db connection failed", "type": type(e).__name__}
    }), 503
