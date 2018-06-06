from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.model import Category, Book, Author, Books_And_Authors, Base

engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

try:
    """
    """
    """
    category = Category(name="history", depth=0, ParentID=0, type='book')
    session.add(category)
    session.commit()

    category = Category(name="biographies & memoirs", depth=0, ParentID=0,
            type='book')
    session.add(category)
    session.commit()
    parent_category = session.query(Category).filter(
        Category.name=="biographies & memoirs",
        Category.depth==0).one()

    category = Category(type='book', name="historical", depth=1,
            ParentID=parent_category.id)
    session.add(category)
    session.commit()

    category = Category(depth=1,
            name='specific groups',
            type='book',
            ParentID=parent_category.id)

    session.add(category)
    session.commit()

    book = Book(
            genre = 'Coming of age',
            page_count = 352,
            name = 'educated: a memoir',
            type = 'book',
            details = An unforgettable memoir about a young girl
            who, kept out of school, leaves her survivalist family
            and goes on to earn a PhD from Cambridge University,
            picture = 'https://images-na.ssl-images-amazon.com/images/I/41eliTRAsHL.jpg',
            rating = '4.5')

    author = Author(
            firstname = 'Tara',
            lastname = 'Westover')

    book.children.append(author)
    book.item_children.append(category)
    session.add(book)
    session.commit()

    author = session.query(Author).filter(Author.firstname == 'Tara').one()
    session.delete(author)
    session.commit()

    book = session.query(Book).filter(Book.rating == '4.5').one()
    session.delete(book)
    session.commit()
    """




except:
    session.rollback()
    raise
