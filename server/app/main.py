from fastapi import Depends, FastAPI, File
from typing import Annotated

from .helpers.math import is_square
from .services.process_level_file import process_levels, unzip_level_files
from .services.finding_words import find_bonus
from . import crud, models, schemas
from .database import SessionLocal, engine
from sqlalchemy.orm import Session  


import math

app = FastAPI()


models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/api/levels")
async def create_file(file: Annotated[bytes, File()], db: Session = Depends(get_db)):
    words, levels = unzip_level_files(file)

    crud.create_words(db, words)

    level_infos = process_levels(words, levels[:10])

    crud.create_levels(db, level_infos)

    return level_infos

# @app.post("/api/bonus")
# async def find_bonuses(db: Session = Depends(get_db)):
#     db_levels = crud.get_levels(db)
#     db_words = crud.get_words(db)
#     words = [db_word.word for db_word in db_words]
#     find_bonus()

@app.get("/api/levels")
async def get_levels(db: Session = Depends(get_db)):
    db_levels = crud.get_levels(db)
    return db_levels

@app.get("/api/words")
async def get_words(db: Session = Depends(get_db)):
    db_words = crud.get_words(db)
    return db_words
