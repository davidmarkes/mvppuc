from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from typing import Union

from model import Base

class Madeira(Base):
    __tablename__ = 'madeiras'

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True, unique=True)
    volume = Column(Integer)
    produto = Column(String)
    origem = Column(String)
