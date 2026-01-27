from datetime import datetime
from flask import jsonify, g
from ..message import RErrorMessage
from ..services.history_service import HistoryService
from ..services.post_lookup_service import PostLookupService

service = HistoryService()
post_lookup = PostLookupService()

def _error_response(message: str, status: int, *, error_type: str | None = None):
  response = RErrorMessage(error_text=message, response_code=status)
  if error_type:
    response.add("type", error_type)
  return response.get()

def _is_published(payload: dict) -> bool:
  # Accept multiple possible shapes from Post service / frontend.
  status = payload.get("postStatus") or payload.get("status") or payload.get("stage")
  if isinstance(status, str):
    return status.strip().lower() == "published"

  if "isPublished" in payload:
    return bool(payload.get("isPublished"))

  if "published" in payload:
    return bool(payload.get("published"))

  # If not provided, assume published (frontend should only call for published posts)
  return True

def _unwrap_post_payload(payload: dict) -> dict:
  if not payload:
    return {}
  if isinstance(payload, dict) and "result" in payload:
    payload = payload.get("result")
  if isinstance(payload, dict) and "post" in payload:
    payload = payload.get("post")
  return payload if isinstance(payload, dict) else {}

def _post_matches_keyword(post_data: dict, keyword: str) -> bool:
  text = " ".join(
    str(post_data.get(field, "") or "")
    for field in ("title", "description", "content", "summary")
  ).lower()
  return keyword.lower() in text

def _merge_history_with_posts(
  items: list[dict], post_payloads: dict, *, require_published: bool = True
) -> list[dict]:
  merged: list[dict] = []
  for item in items:
    post_id = str(item.get("postId"))
    payload = _unwrap_post_payload(post_payloads.get(post_id, {}))
    if not payload:
      continue
    if require_published and not _is_published(payload):
      continue
    merged.append({**item, "post": payload})
  return merged

def _parse_view_date(value: str | None) -> datetime | None:
  if not value:
    return None
  try:
    return datetime.strptime(value, "%Y-%m-%d")
  except ValueError:
    return None

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
    date_value = (req.args.get("date") or "").strip()
    parsed_date = _parse_view_date(date_value)
    if date_value and not parsed_date:
      return _error_response("date must be in YYYY-MM-DD format", 400)

    items = (
      service.list_by_user_on_date(user_id=user_id, view_date=parsed_date)
      if parsed_date
      else service.list_by_user(user_id=user_id)
    )
    keyword = (req.args.get("keyword") or "").strip()
    post_ids = [str(item.get("postId")) for item in items if item.get("postId")]
    post_payloads = (
      post_lookup.fetch_posts_by_ids(post_ids, req.headers.get("Authorization"))
      if post_ids
      else {}
    )

    if post_payloads:
      items = _merge_history_with_posts(items, post_payloads, require_published=True)
      if keyword:
        items = [
          item
          for item in items
          if _post_matches_keyword(item.get("post") or {}, keyword)
        ]
    elif keyword:
      items = []

    return jsonify({"result": items}), 200
  except Exception as e:
    return _error_response(
      "db operation failed",
      503,
      error_type=type(e).__name__,
    )
