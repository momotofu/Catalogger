from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.model import Categories, Book, Author, Books_And_Authors, Base

engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

"""
category = Categories(name="history", depth=0, child_id=0)
session.add(category)
session.commit()

category = Categories(name="biographies & memoirs", depth=0, child_id=0)
session.add(category)
session.commit()
"""

try:
    """
    category = Categories(name="historical", depth=1, child_id=0)
    session.add(category)
    session.commit()
    """

    parent_category = session.query(Categories).filter(
        Categories.name=="biographies & memoirs",
        Categories.depth==0).one()

    category = session.query(Categories).filter(
        Categories.name=="historical",
        Categories.depth==1,
        Categories.child_id==0).one()
    parent_category.child_id = category.id
    session.add(parent_category)
    session.commit()
except:
    raise





