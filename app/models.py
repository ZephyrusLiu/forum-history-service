from .db import db
from datetime import datetime

class History(db.Model):
  __tablename__ = "history"

  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.String(64), nullable=False)
  post_id = db.Column(db.String(64), nullable=False)
  created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

  def to_dict(self):
    return {
      "id": self.id,
      "userId": self.user_id,
      "postId": self.post_id,
      "createdAt": self.created_at.isoformat()
    }
