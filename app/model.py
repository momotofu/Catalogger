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

class A0_Categories(Base):
    __tablename__ = 'a_0_categories'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)

# Intermediary table
class A0_to_A1_Categories(Base):
    __tablename__ = 'a0_to_a1_categories'

    id = Column(Integer, primary_key=True)
    category_id = Column(Integer, ForeignKey('a0_categories.id'))
    subcategory_id = Column(Integer, ForeignKey('a1_categories.id'))

    # Relationships
    a0_categories = relationship(A0_Categories)
    a1_categories = relationship(A1_Categories)


class A1_Categories(Base):
    __tablename__ = 'a_1_categories'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)


class Item(Base):
    __tablename__ = 'item'

    # attributes
    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    details = Column(String(400))
    picture = Column(String(200))
    category_id = Column(Integer, ForeignKey('category.id'))
    user_id = Column(Integer, ForeignKey('user.id'))

    # relationships
    category = relationship(Category)
    user = relationship(User)

engine = create_engine("sqlite:///catalog.db")
Base.metadata.create_all(engine)
