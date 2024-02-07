"""
CRUD features for stuff.
"""

from sqlalchemy.orm import Session
from sqlalchemy import text

def check_alive(db: Session):
    try:
        db.execute(text('SELECT 1'))
        return True
    except Exception as e:
        return False

