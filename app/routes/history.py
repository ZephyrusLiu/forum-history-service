from flask import Blueprint, request
from utils.python.auth import login_required
from ..controllers.history_controller import create_history, list_history

history_bp = Blueprint("history", __name__)

@history_bp.post("")
@login_required
def post_history():
  return create_history(request)

@history_bp.get("")
@login_required
def get_history():
  return list_history(request)
