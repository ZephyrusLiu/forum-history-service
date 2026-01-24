from flask import jsonify, g
from ..message import RErrorMessage
from ..services.history_service import HistoryService

service = HistoryService()

def _error_response(message: str, status: int, *, error_type: str | None = None):
  response = RErrorMessage(error_text=message, response_code=status)
  if error_type:
    response.add("type", error_type)
  return response.get()

def _is_published(payload: dict) -> bool:
  # Accept multiple possible shapes from Post service / frontend.
  status = payload.get("postStatus") or payload.get("status")
  if isinstance(status, str):
    return status.strip().lower() == "published"

  if "isPublished" in payload:
    return bool(payload.get("isPublished"))

  if "published" in payload:
    return bool(payload.get("published"))

  # If not provided, assume published (frontend should only call for published posts)
  return True

def create_history(req):
  data = req.get_json(silent=True) or {}
  post_id = data.get("postId") or data.get("post_id")

  if not post_id:
    return _error_response("postId is required", 400)

  # Enforce: only Published posts are recorded.
  if not _is_published(data):
    return jsonify({"result": None, "skipped": True}), 200

  user_id = (g.user or {}).get("userId")
  if not user_id:
    return _error_response("Missing userId in token", 401)

  try:
    created = service.create(user_id=user_id, post_id=str(post_id))
    return jsonify({"result": created}), 201
  except Exception as e:
    return _error_response(
      "db operation failed",
      503,
      error_type=type(e).__name__,
    )

def list_history(req):
  user_id = (g.user or {}).get("userId")
  if not user_id:
    return _error_response("Missing userId in token", 401)

  try:
    items = service.list_by_user(user_id=user_id)
    return jsonify({"result": items}), 200
  except Exception as e:
    return _error_response(
      "db operation failed",
      503,
      error_type=type(e).__name__,
    )
