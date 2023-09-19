from sqlalchemy import Column, Integer, String, JSON

from .database import Base

class Words(Base):
    __tablename__ = "words"

    id = Column(Integer, primary_key=True, index=True)
    word = Column(String, unique=True)

class Levels(Base):
    __tablename__ = "levels"

    id = Column(Integer, primary_key=True, index=True)
    path = Column(String, unique=True)
    status = Column(String, nullable=True)
    bonus = Column(String, nullable=True)
    words = Column(String, nullable=True)
