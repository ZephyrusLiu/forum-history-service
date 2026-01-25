from __future__ import annotations

from typing import Any
import requests
from flask import current_app


class PostLookupService:
  def __init__(self, timeout_seconds: float = 3.0):
    self.timeout_seconds = timeout_seconds

  def fetch_posts_by_ids(self, post_ids: list[str], auth_header: str | None) -> dict[str, Any]:
    base_url = (current_app.config.get("POST_SERVICE_URL") or "").rstrip("/")
    if not base_url:
      return {}

    headers = {}
    if auth_header:
      headers["Authorization"] = auth_header

    results: dict[str, Any] = {}
    for post_id in post_ids:
      url = f"{base_url}/posts/{post_id}"
      try:
        resp = requests.get(url, headers=headers, timeout=self.timeout_seconds)
      except requests.RequestException:
        continue

      if resp.status_code != 200:
        continue

      try:
        payload = resp.json()
      except ValueError:
        continue

      results[str(post_id)] = payload

    return results
