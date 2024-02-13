"""
CRUD features for stuff.
"""
import datetime
from sqlalchemy.orm import Session
from pydantic import PositiveInt
from my_api.schemas import CreatePost
from my_api.models import Post


def check_alive(db: Session):
    num = db.query(Post).count()
    return num


def get_post_by_id(db: Session, p_id: PositiveInt) -> Post | None:
    result = db.query(Post).filter(Post.id == p_id).first()
    return result


def create_post(db: Session, p_info: CreatePost) -> Post | None:
    db_post = Post(**p_info.model_dump())
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


def delete_post(db: Session, p_id: PositiveInt) -> Post:
    db_post = get_post_by_id(db, p_id)
    if db_post is None:
        return None
    db.delete(db_post)
    db.commit()
    return db_post

def ghost_delete_post(db: Session, p_id: PositiveInt) -> Post:
    db_post = get_post_by_id(db, p_id)
    if db_post is None:
        return None
    db_post.is_deleted = True
    db_post.date_modified = datetime.datetime.utcnow()
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post