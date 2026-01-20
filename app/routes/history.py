from flask import Blueprint, request
from ..controllers.history_controller import create_history, list_history

history_bp = Blueprint("history", __name__)

@history_bp.post("")
def post_history():
  return create_history(request)

@history_bp.get("")
def get_history():
  return list_history(request)
