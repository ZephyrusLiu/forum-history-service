from .db import db
from datetime import datetime

class History(db.Model):
  __tablename__ = "history"

  history_id = db.Column("historyId", db.Integer, primary_key=True)
  user_id = db.Column("userId", db.String(64), nullable=False)
  post_id = db.Column("postId", db.String(64), nullable=False)
  view_date = db.Column("viewDate", db.DateTime, default=datetime.utcnow, nullable=False)

  def to_dict(self):
    return {
      "historyId": self.history_id,
      "userId": self.user_id,
      "postId": self.post_id,
      "viewDate": self.view_date.isoformat()
    }
