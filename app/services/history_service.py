from ..db import db
from ..models import History

class HistoryService:
  def create(self, user_id: str, post_id: str):
    h = History(user_id=user_id, post_id=post_id)
    db.session.add(h)
    db.session.commit()
    return h.to_dict()

  def list_by_user(self, user_id: str):
    items = (
      History.query.filter_by(user_id=user_id)
      .order_by(History.created_at.desc())
      .all()
    )
    return [x.to_dict() for x in items]
