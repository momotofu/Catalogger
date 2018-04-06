from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    # attributes
    id = Column(Integer, primary_key=True)
    firstname = Column(String(80))
    lastname = Column(String(80))
    email = Column(String(80), nullable=False)
    picture = Column(String(80))
    username = Column(String(80))
    password_hash = Column(String(64))


class Categories(Base):
    __tablename__ = 'categories'

    # attributes
    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    child_id = Column(Integer, ForeignKey('categories.id'))

    # relationships
    categories = relationship('categories')


class Item(Base):
    __tablename__ = 'item'

    # attributes
    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    details = Column(String(400))
    picture = Column(String(200))
    rating = Column(Integer)

    category_id = Column(Integer, ForeignKey('categories.id'))
    user_id = Column(Integer, ForeignKey('user.id'))

    # relationships
    category = relationship(Categories)
    user = relationship(User)


class Book(Item):
    __tablename__ = 'book'

    # attributes
    id = Column(Integer, ForeignKey('item.id'), primary_key=True)
    __mapper_args__ = {'polymorphic_identity':'book',
                       'inherit_condition': (id == Item.id)}
    genre = Column(String(80))
    page_count = Column(Integer)


class Author(Base):
    __tablename__ = 'author'

    # attributes
    id = Column(Integer, primary_key=True)
    firstname = Column(String(80), nullable=False)
    middlename = Column(String(80))
    lastname = Column(String(80))


class Books_And_Authors(Base):
    __tablename__ = 'books_and_authors'

    # attributes
    id = Column(Integer, primary_key=True)
    book_id = Column(ForeignKey('book.id'), nullable=False)
    author_id = Column(ForeignKey('author.id'), nullable=False)


engine = create_engine("sqlite:///catalog.db")
Base.metadata.create_all(engine)
