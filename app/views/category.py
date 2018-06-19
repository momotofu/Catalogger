from app.model import Category, Item, Items_And_Categories
from app.app import session
from flask import Blueprint, render_template, request
from flask import current_app as app
from flask_login import current_user

import json, os

category = Blueprint('category',
                        __name__,
                        template_folder='templates')


@category.route('/')
@category.route('/categories')
def allCategories():
    if current_user.is_authenticated:
        # get all user items
        items = (
                session.query(Category)
                .filter(Item.user_id == current_user.id)
        )
         # s = session.query(Category).join(Items_And_Categories).join(Item).filter(Item.user_id == current_user.id)
        # get all item categories
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
            depth=0)
    else:
        return json.dumps({'error': 'missing name parameter'}), 422

    try:
        # add new category to the database
        session.add(category)
        session.commit()

        return json.dumps(category.serialize)

    except:
        session.rollback()
        raise

        return json.dumps({'error': 'failed to create a category'}), 400


@category.route('/categories/<int:category_id>/delete', methods=['POST'])
def deleteCategory(category_id):
    try:
        category = session.query(Category).filter(Category.id == category_id).one()
        items = (
            session.query(Item)
                .join(Item.item_children)
                .filter(Category.id == category_id)
                .all()
        )

        session.delete(category)

        # if items have no categories then remove them
        for item in items:
            print('children len: ', item.item_children, len(item.item_children))
            if len(item.item_children) == 0:
                os.remove(os.path.join(app.config['IMAGE_FOLDER'], item.image_name))
                session.delete(item)

        # commit changes to the database
        session.commit()

        return json.dumps({'name': category.name, 'success':True}), 200, {'Conten Type':'application/json'}

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
