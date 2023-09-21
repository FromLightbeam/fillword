import itertools
from multiprocessing import Pool
from fastapi import Depends, FastAPI, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Annotated

import requests

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
async def create_levels_from_file(params: schemas.CreateLevelBody, db: Session = Depends(get_db)):
    try:
        response = requests.get(params.url)
        words, levels = unzip_level_files(response.content)
    except:
        raise HTTPException(status_code=400, detail="Error while unzipping file")

    crud.create_words(db, words)

    level_infos = process_levels(words, levels)
    crud.create_levels(db, level_infos)

    return list(filter(lambda level: level['status'] != 'valid', level_infos))

def find_bonus_pfunc(params):
    level, all_words = params
    bonus_words = find_bonus(all_words, level.matrix, level.words)
    return bonus_words

@app.post("/api/bonus")
async def find_bonuses(params: schemas.FindBonusBody, db: Session = Depends(get_db)):
    db_levels, total_count = crud.get_levels(db, params.offset, params.limit)
    db_words = crud.get_words(db)
    all_words = [db_word.word for db_word in db_words]

    with Pool(8) as p:
        bonus_words = p.map(find_bonus_pfunc, list(zip(db_levels, itertools.repeat(all_words))))
    for bonus, db_level in zip(bonus_words, db_levels):
        db_level.bonus_words = bonus
    db.commit()

    db_levels, total_count = crud.get_levels(db, params.offset, params.limit)
    return { "levels": db_levels, "total_count": total_count }

@app.get("/api/levels")
async def get_levels(offset: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    db_levels, total_count = crud.get_levels(db, offset, limit)
    return { "levels": db_levels, "total_count": total_count }
