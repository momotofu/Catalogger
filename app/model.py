from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    firstname = Column(String(80))
    lastname = Column(String(80))
    email = Column(String(80), nullable=False)
    picture = Column(String(80))
    username = Column(String(80))
    password_hash = Column(String(64))

class Categories(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    child_id = Column(Integer, ForeignKey('categories.id'))

    # Relationships
    categories = relationship('categories')


class Item(Base):
    __tablename__ = 'item'

    # attributes
    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    details = Column(String(400))
    picture = Column(String(200))
    category_id = Column(Integer, ForeignKey('categories.id'))
    user_id = Column(Integer, ForeignKey('user.id'))

    # relationships
    category = relationship(Categories)
    user = relationship(User)

engine = create_engine("sqlite:///catalog.db")
Base.metadata.create_all(engine)
