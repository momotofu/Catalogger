from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy import UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
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
        ondelete='CASCADE'),
        nullable=False)

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
    name = Column(String(80), nullable=False)
    type = Column(String(80), nullable=False)
    details = Column(String(400))
    picture = Column(String(200))
    rating = Column(String(3))
    user_id = Column(Integer, ForeignKey('user.id'))

    # relationships
    user = relationship(User)
    item_children = relationship('Category',
            secondary='items_and_categories',
            cascade='all')


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
    book_id = Column(ForeignKey('book.id'), primary_key=True)
    author_id = Column(ForeignKey('author.id'), primary_key=True)

    # relationships
    book = relationship('Book')
    author = relationship('Author')


class Items_And_Categories(Base):
    __tablename__ = 'items_and_categories'

    # attributes
    category_id = Column(ForeignKey('category.id'), primary_key=True)
    item_id = Column(ForeignKey('item.id'), primary_key=True)

    # relationships
    item = relationship('Item')
    category = relationship('Category')



engine = create_engine('sqlite:///catalog.db')
Base.metadata.create_all(engine)
