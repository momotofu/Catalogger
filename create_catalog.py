from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.model import Categories, Book, Author, Books_And_Authors, Base

engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()
"""
category = Categories(name="history", depth=0, ParentID=0)
session.add(category)
session.commit()

category = Categories(name="biographies & memoirs", depth=0, ParentID=0)
session.add(category)
session.commit()
"""
try:
    parent_category = session.query(Categories).filter(
        Categories.name=="biographies & memoirs",
        Categories.depth==0).one()

    """
    category = Categories(name="historical", depth=1,
            ParentID=parent_category.id)
    session.add(category)
    session.commit()
    """


    """
    category = session.query(Categories).filter(
        Categories.name=="historical",
        Categories.depth==1,
        Categories.ParentID==0).one()
    category.ParentID = parent_category.id
    session.add(category)
    session.commit()

    """
    session.delete(parent_category)
    session.commit()
except:
    raise





