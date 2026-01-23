import os
from dotenv import load_dotenv

# Load .env BEFORE importing app factory/config
BASE_DIR = os.path.dirname(__file__)
dotenv_path = os.path.join(BASE_DIR, ".env")
if os.path.exists(dotenv_path):
  load_dotenv(dotenv_path=dotenv_path, override=False)

from app.app_factory import create_app

app = create_app()

if __name__ == "__main__":
  port = int(os.getenv("SERVICE_PORT", "5003"))
  app.run(host="0.0.0.0", port=port)
