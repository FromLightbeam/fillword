from sqlalchemy import insert
from sqlalchemy.orm import Session

from . import models


def get_levels(db: Session, offset: int, limit: int):
    db_levels = db.query(models.Levels).offset(offset).limit(limit).all()
    total_count = db.query(models.Levels).count()
    return db_levels, total_count


def get_words(db: Session):
    return db.query(models.Words).all()


def create_words(db: Session, words: list[str]):
    stmt = insert(models.Words).values([{'word': word} for word in words]).prefix_with('OR IGNORE')
    db.execute(stmt)
    db.commit()


def create_levels(db: Session, levels):
    stmt = insert(models.Levels).values([{
        'matrix': level["matrix"],
        'words': level['words'],
        'bonus_words': [],
        'status': level['status'],
        'filename': level['filename'],
    } for level in levels]).prefix_with('OR IGNORE')
    db.execute(stmt)
    db.commit()
