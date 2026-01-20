from flask import jsonify
from ..services.history_service import HistoryService

service = HistoryService()

def create_history(req):
  data = req.get_json(silent=True) or {}
  user_id = data.get("userId")
  post_id = data.get("postId")

  if not user_id or not post_id:
    return jsonify({
      "error": {"code": "VALIDATION_ERROR", "message": "userId and postId are required"}
    }), 400

  item = service.create(user_id=user_id, post_id=post_id)
  return jsonify({"result": item}), 201

def list_history(req):
  user_id = req.args.get("userId")
  if not user_id:
    return jsonify({
      "error": {"code": "VALIDATION_ERROR", "message": "userId query param is required"}
    }), 400

  items = service.list_by_user(user_id=user_id)
  return jsonify({"result": items}), 200
