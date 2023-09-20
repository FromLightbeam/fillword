from sqlalchemy import Column, Integer, String, JSON

from .database import Base

class Words(Base):
    __tablename__ = "words"

    id = Column(Integer, primary_key=True, index=True)
    word = Column(String, unique=True)

class Levels(Base):
    __tablename__ = "levels"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=True)
    matrix = Column(JSON, unique=True)
    status = Column(String, nullable=True)
    bonus_words = Column(JSON, nullable=True)
    words = Column(JSON, nullable=True)
