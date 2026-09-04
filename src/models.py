from sqlalchemy import Column, Integer, String, Text

from m30.src.database import Base


class Recipe(Base):
    __tablename__ = "Recipe"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text, index=True, nullable=True)
    cooking_time = Column(Integer, index=True)
    ingredients = Column(String, index=True)
    views = Column(Integer, default=0, index=True)
