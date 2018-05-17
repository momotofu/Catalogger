from app.model import Category
from app.utils.utils import get_session
from flask import Blueprint, render_template, request
import json

session = get_session('sqlite:///catalog.db')
category = Blueprint('category',
                        __name__,
                        template_folder='templates')


@category.route('/')
@category.route('/categories')
def allCategories():
    # grab categories from database
    categories = session.query(Category).filter(Category.depth == 0).all()

    # serialize and prepare category objects for json
    categories_serialized = [category.serialize for category in categories]
    categories_serialized.reverse()

    return render_template('category/index.html', categories=json.dumps(categories_serialized))


@category.route('/categories/new', methods=['POST'])
def newCategory():
    params = request.form

    # ensure name key and name value
    if 'name' in params.keys():
        name = params['name']

        category = Category(
            name=name,
            type=name,
            depth=0,
            ParentID=0)
    else:
        return

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


@category.route('/categories/<int:category_id>/delete', methods=['POST'])
def deleteCategory(category_id):
    try:
        session.query(Category).filter(Category.id == category_id).delete()
        session.commit()

        return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

    except:
        session.rollback()
        raise


@category.route('/categories/update', methods=['POST'])
def updateCategories():
    categories = json.loads(request.form['categories'])

    try:
        for data in categories:
            for key in data.keys():
                # get an ORM'd reference to current category
                category = session.query(Category).filter(Category.id ==
                        data['id']).one()

                # update the category properties
                category.name = data['name']
                category.type = data['type']
                category.depth = data['depth']
                category.ParentID = data['parentId']

                # commit changes to the database
                session.commit()

        return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

    except:
        session.rollback()
        raise
