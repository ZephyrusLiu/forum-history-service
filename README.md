# History Service (Flask) — Day 3 (D3-YL-1)

This service records a logged-in user’s browsing history for **Published** posts only.

## Key Rules (AC)
- **JWT is required** for `POST /history` and `GET /history`.
- JWT is **validated inside this service** (service-level auth), not only relying on Gateway.
- Only **Published** posts are recorded and displayed.
- `GET /history` returns **descending** order (most recent first).

## Routes
- `GET /health` -> `{ "status": "ok" }`
- `POST /history`
  - Body accepts either:
    - `{ "postId": 123, "postStatus": "Published" }`
    - or `{ "postId": 123, "published": true }`
  - If not published => returns `{ result: null, skipped: true }` and does **not** write DB.
- `GET /history`
  - Returns `{ result: [...] }` with newest first.
- `GET /history?keyword=<word>`
  - Performs keyword search by fetching post details from Post service and
    matching against `title/description/content` (case-insensitive).
  - Returns only **Published** posts that match the keyword.

## Run locally
```bash
python -m venv .venv
Mac:
source .venv/bin/activate
Win:
.\.venv\Scripts\activate
pip install -r requirements.txt
