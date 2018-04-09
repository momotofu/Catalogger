from app.model import Category
from app.utils.utils import get_session
from flask import Blueprint

session = get_session('sqlite:///catalog.db')
category = Blueprint('category',
                        __name__,
                        template_folder='templates')


@category.route('/')
@category.route('/')
def allCategories():
    categories = session.query(Category).filter(Category.depth == 0).all()
    return render_template('category/index.html', categories=categories)

