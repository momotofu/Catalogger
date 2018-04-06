from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.model import Categories, Book, Author, Books_And_Authors, Base

engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


category = Categories(name="history", depth=0, child_id=0)
session.add(category)
session.commit()

category = Categories(name="biographies & memoirs", depth=0, child_id=0)
session.add(category)
session.commit()

try:
    parent_category = session.query(Categories).filter(
        Categories.name=="biographies & memoirs",
        Categories.depth==0).one()
    print("parent_category: ", parent_category)
    category = Categories(name="historical", depth=1, child_id=0)
    parent_category.child_id = category.id
    session.add(category)
    session.add(parent_category)
    session.commit()
except:
    raise





