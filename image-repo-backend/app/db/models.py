from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(100))
    username = Column(String(100), unique=True, index=True)
    password = Column(String(100))
    token = Column(String(100), index=True)

    images = relationship("Images", back_populates="owner")

class Images(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    owner_id = Column(Integer, ForeignKey("users.id"))
    is_public = Column(Boolean, default=True)

    owner = relationship("User", back_populates="images")