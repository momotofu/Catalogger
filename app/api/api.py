from flask import Blueprint, send_from_directory
from flask_login import current_user

from app.app import session
from app.model import Category, Item

import json, os

api = Blueprint('api',
                        __name__,
                        template_folder='templates')

# API for local assets
@api.route('/images', defaults={'filename': 'filler.jpg'})
@api.route('/images/<filename>')
def image_file(filename):
    return send_from_directory('static/images', filename)


@api.route('/build/public/<filename>')
def getAsset(filename):
    return send_from_directory(os.path.abspath('build/public'), filename)


# API data endpoints
@api.route('/categories/JSON')
def getCategories():
    if current_user.is_authenticated:
        # grab user specific categories from the database
        categories = (
                session.query(Category)
                .filter(Category.user_id == current_user.id)
                .all())
    else:
        # grab public categories from the database
        categories = (
                session.query(Category)
                .filter(Category.user_id == None)
                .all())

    # serialize and prepare category objects for json
    serialized_categories = [category.serialize for category in categories]
    serialized_categories.reverse()

    return json.dumps(serialized_categories), 200


@api.route('/category/<int:category_id>/items/JSON')
def getItems(category_id):
    try:
        if current_user.is_authenticated:
            items = (
                session.query(Item)
                .filter(Item.user_id == current_user.id)
                .join(Item.item_children)
                .filter(Category.id == category_id)
                .all())
        else:
            items = (
                session.query(Item)
                .filter(Item.user_id == None)
                .join(Item.item_children)
                .filter(Category.id == category_id)
                .all())

        return json.dumps([item.serialize for item in items])

    except:
        return json.dumps({'error': 'unable to fetch items'}), 400


@api.route('/items/<int:item_id>/JSON')
def getItem(item_id):
    try:
        # grab on ORM reference to the item
        item = (
            session.query(Item)
            .filter(Item.id == item_id)
            .one())

        # restrict access if item is associated with a user
        if item.user_id and not current_user.is_authenticated:
            return json.dumps({
                'error': 'you do not have access to this item'}), 400
        else:
            return json.dumps(item.serialize)

    except:
        return json.dumps({'error': 'unable to fetch items'}), 400
