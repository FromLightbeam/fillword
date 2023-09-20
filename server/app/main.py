import json
from fastapi import Depends, FastAPI, File
from fastapi.middleware.cors import CORSMiddleware
from typing import Annotated

from .helpers.math import is_square
from .services.process_level_file import process_levels, unzip_level_files
from .services.finding_words import find_bonus
from . import crud, models, schemas
from .database import SessionLocal, engine
from sqlalchemy.orm import Session  

app = FastAPI()

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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

@app.post("/api/bonus")
async def find_bonuses(params: schemas.FindBonusBody, db: Session = Depends(get_db)):
    db_levels = crud.get_levels(db, params.offset, params.limit)
    db_words = crud.get_words(db)
    all_words = [db_word.word for db_word in db_words]
    for db_level in db_levels:
        bonus_words = find_bonus(all_words, db_level.matrix, db_level.words)
        db_level.bonus_words = bonus_words
    db.commit()

    db_levels = crud.get_levels(db, params.offset, params.limit)
    return db_levels

@app.get("/api/levels")
async def get_levels(offset: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    level_infos = crud.get_levels(db, offset, limit)
    return level_infos

@app.get("/api/words")
async def get_words(db: Session = Depends(get_db)):
    db_words = crud.get_words(db)
    return db_words
