from datetime import datetime, timedelta
from ..db import db
from ..models import History

class HistoryService:
  def create(self, user_id: str, post_id: str):
    try:
      h = History(user_id=user_id, post_id=post_id)
      db.session.add(h)
      db.session.commit()
      return h.to_dict()
    except Exception:
      try:
        db.session.rollback()
      except Exception:
        pass
      raise

  def list_by_user(self, user_id: str):
    try:
      items = (
        History.query.filter_by(user_id=user_id)
        .order_by(History.view_date.desc())
        .all()
      )
      return [x.to_dict() for x in items]
    except Exception:
      try:
        db.session.rollback()
      except Exception:
        pass
      raise

  def list_by_user_on_date(self, user_id: str, view_date: datetime):
    try:
      start = datetime(view_date.year, view_date.month, view_date.day)
      end = start + timedelta(days=1)
      items = (
        History.query.filter(History.user_id == user_id)
        .filter(History.view_date >= start)
        .filter(History.view_date < end)
        .order_by(History.view_date.desc())
        .all()
      )
      return [x.to_dict() for x in items]
    except Exception:
      try:
        db.session.rollback()
      except Exception:
        pass
      raise

  def list_by_user_paginated(self, user_id: str, page: int, page_size: int):
    try:
      query = History.query.filter_by(user_id=user_id)
      total = query.count()
      items = (
        query.order_by(History.view_date.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
      )
      return [x.to_dict() for x in items], total
    except Exception:
      try:
        db.session.rollback()
      except Exception:
        pass
      raise

  def list_by_user_on_date_paginated(
    self, user_id: str, view_date: datetime, page: int, page_size: int
  ):
    try:
      start = datetime(view_date.year, view_date.month, view_date.day)
      end = start + timedelta(days=1)
      query = (
        History.query.filter(History.user_id == user_id)
        .filter(History.view_date >= start)
        .filter(History.view_date < end)
      )
      total = query.count()
      items = (
        query.order_by(History.view_date.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
      )
      return [x.to_dict() for x in items], total
    except Exception:
      try:
        db.session.rollback()
      except Exception:
        pass
      raise
