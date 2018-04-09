import random, string
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.model import Base



def allowed_file(filename, app):
    return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


def get_rand_string():
    return ''.join(random.choice(string.ascii_uppercase + string.digits +
        string.ascii_lowercase) for x in range(32))


def get_session(db_path):
    """
    returns an sqlalchemy session.
    """

    engine = create_engine('sqlite:///restaurantmenu.db')
    Base.metadata.bind = engine

    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    return session
