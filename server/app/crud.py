import json
from sqlalchemy import insert
from sqlalchemy.orm import Session

from .database import engine, SessionLocal

from . import models, schemas


def get_levels(db: Session):
    db_levels = db.query(models.Levels).all()
    return db_levels, [{
        'matrix': json.loads(level.path),
        'words': json.loads(level.words),
        'bonus': json.loads(level.bonus),
    } for level in db_levels]


def get_words(db: Session):
    return db.query(models.Words).all()


def create_words(db: Session, words: list[str]):
    stmt = insert(models.Words).values([{'word': word} for word in words]).prefix_with('OR IGNORE')
    db.execute(stmt)
    db.commit()


def create_levels(db: Session, levels: list[str]):
    # print('levels', level['words'])
    # TODO use JSON field
    stmt = insert(models.Levels).values([{
        'path': json.dumps(level["matrix"]),
        'words': json.dumps(level['words']),
        'bonus': json.dumps([]),
    } for level in levels]).prefix_with('OR IGNORE')
    db.execute(stmt)
    db.commit()
