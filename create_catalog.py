from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.model import Categories, Book, Author, Books_And_Authors, Base

engine = create_engine('sqlite:///catalog.db', echo=True)
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


category = Categories(name="history", child_id=20, is_child=False)
session.add(category)
session.commit()

category = Categories(name="biographies & memoirs", is_child=False)
session.add(category)
session.commit()

parent_category = session.query(Categories).filter(
category = Categories(name="historical", child_id=None, is_child=True)
session.add(category)
session.commit()





