import os
from dotenv import load_dotenv

# Load .env BEFORE importing app factory/config
BASE_DIR = os.path.dirname(__file__)
REPO_ROOT = os.path.abspath(os.path.join(BASE_DIR, os.pardir))
root_env = os.path.join(REPO_ROOT, ".env")
service_env = os.path.join(BASE_DIR, ".env")
if os.path.exists(root_env):
  load_dotenv(dotenv_path=root_env, override=False)
if os.path.exists(service_env):
  load_dotenv(dotenv_path=service_env, override=False)

from app.app_factory import create_app

app = create_app()

if __name__ == "__main__":
  port = int(os.getenv("SERVICE_PORT", "5003"))
  app.run(host="0.0.0.0", port=port)
