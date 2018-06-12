from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy import UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy import create_engine
from sqlalchemy import event
from sqlalchemy.engine import Engine

from sqlite3 import Connection as SQLite3Connection

Base = declarative_base()


@event.listens_for(Engine, "connect")
def _set_sqlite_pragma(dbapi_connection, connection_record):
    if isinstance(dbapi_connection, SQLite3Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON;")
        cursor.close()


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
    authenticated = Column(Boolean(False), nullable=False)

    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.email

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False


class Category(Base):
    __tablename__ = 'category'
    __table_args__ = (UniqueConstraint('name', 'depth', 'ParentID',
        name='table_constraint'),)

    # attributes
    id = Column(Integer, primary_key=True)
    depth = Column(Integer, nullable=False)
    name = Column(String(80), nullable=False)
    type = Column(String(80), nullable=False)
    ParentID = Column(Integer,
        ForeignKey('category.id',
        ondelete='CASCADE'))

    # relationships
    Children = relationship('Category',
        cascade="all",
        backref=backref('Parent', remote_side=[id]))

    @property
    def serialize(self):
        # returns object data in easily serializeable format
        return {
            'id' : self.id,
            'name' : self.name,
            'depth' : self.depth,
            'type' : self.type,
            'parentId' : self.ParentID
        }



class Item(Base):
    __tablename__ = 'item'

    # attributes
    id = Column(Integer, primary_key=True)
    type = Column(String(80), nullable=False)
    name = Column(String(80), nullable=False)
    image_name = Column(String(80))
    details = Column(String(400))
    rating = Column(String(3))
    user_id = Column(Integer, ForeignKey('user.id'))

    # relationships
    user = relationship(User)
    item_children = relationship('Category',
            secondary='items_and_categories',
            cascade='all')

    @property
    def serialize(self):
        # returns object data in easily serializeable format
        return {
            'id' : self.id,
            'type' : self.type,
            'name' : self.name,
            'image_name' : self.image_name,
            'details' : self.details.strip(),
            'rating' : self.rating,
            'user_id' : self.user_id,
            'categories_ids' : [category.id for category in self.item_children]
        }


class Book(Item):
    __tablename__ = 'book'

    # attributes
    id = Column(Integer, ForeignKey('item.id'), primary_key=True)
    genre = Column(String(80))
    page_count = Column(Integer)

    # relationships
    children = relationship('Author',
            secondary='books_and_authors',
            cascade='all')

    __mapper_args__ = {'polymorphic_identity':'book',
                       'inherit_condition': (id == Item.id)}

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
    book_id = Column(ForeignKey('book.id', onupdate='CASCADE', ondelete='CASCADE'), primary_key=True)
    author_id = Column(ForeignKey('author.id', onupdate='CASCADE', ondelete='CASCADE'), primary_key=True)

    # relationships
    book = relationship('Book')
    author = relationship('Author')


class Items_And_Categories(Base):
    __tablename__ = 'items_and_categories'

    # attributes
    category_id = Column(ForeignKey('category.id', onupdate='CASCADE', ondelete='CASCADE'), primary_key=True)
    item_id = Column(ForeignKey('item.id', onupdate='CASCADE', ondelete='CASCADE'), primary_key=True)

    # relationships
    item = relationship('Item')
    category = relationship('Category')


engine = create_engine('sqlite:///catalog.db')
Base.metadata.create_all(engine)
