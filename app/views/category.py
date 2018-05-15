from app.model import Category
from app.utils.utils import get_session
from flask import Blueprint, render_template
import json

session = get_session('sqlite:///catalog.db')
category = Blueprint('category',
                        __name__,
                        template_folder='templates')


@category.route('/')
@category.route('/categories')
def allCategories():
    categories = session.query(Category).filter(Category.depth == 0).all()
    return render_template('category/index.html',
            categories=json.dumps([category.serialize for category in categories]))


@category.route('/categories/new', methods=['POST'])
def newCategory():
    name = request.args.get('name')
    category = Category(
        name=name,
        type=name,
        depth=0,
        parentID=0)

    try:
        # add new category to the database
        session.add(category)
        session.commit()

        # return item with database given id
        category = session.query(Category).filter(Category.name == category.name).one()
        return json.dumps(category.serialize)

    except:
        session.rollback()
        raise



