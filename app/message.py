from __future__ import annotations

import os
import sys

try:
  from utils.python.message import Message
except ModuleNotFoundError:
  base_dir = os.path.dirname(os.path.abspath(__file__))
  repo_root = os.path.abspath(os.path.join(base_dir, os.pardir, os.pardir))
  if repo_root not in sys.path:
    sys.path.insert(0, repo_root)
  from utils.python.message import Message

__all__ = ["Message"]
