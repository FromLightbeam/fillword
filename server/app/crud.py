import json
from sqlalchemy import insert
from sqlalchemy.orm import Session

from .database import engine, SessionLocal

from . import models, schemas


def get_levels(db: Session, offset: int, limit: int):
    db_levels = db.query(models.Levels).offset(offset).limit(limit).all()
    return db_levels


def get_words(db: Session):
    return db.query(models.Words).all()


def create_words(db: Session, words: list[str]):
    stmt = insert(models.Words).values([{'word': word} for word in words]).prefix_with('OR IGNORE')
    db.execute(stmt)
    db.commit()


def create_levels(db: Session, levels: list[str]):
    stmt = insert(models.Levels).values([{
        'matrix': level["matrix"],
        'words': level['words'],
        'bonus_words': [],
    } for level in levels]).prefix_with('OR IGNORE')
    db.execute(stmt)
    db.commit()
