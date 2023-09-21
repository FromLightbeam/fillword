from pydantic import BaseModel


class WordsBase(BaseModel):
    word: str
    class Config:
        orm_mode = True

class LevelBase(BaseModel):
    path: list
    status: str
    bonus: str

class LevelCreate(LevelBase):
    pass

class Level(LevelBase):
    id: int


class FindBonusBody(BaseModel):
    limit: int
    offset: int

class CreateLevelBody(BaseModel):
    url: str
