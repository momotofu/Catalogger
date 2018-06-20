from flask import Blueprint, send_from_directory
from flask_login import current_user

from app.app import session
from app.model import Category

import json

api = Blueprint('api',
                        __name__,
                        template_folder='templates')


# API endpoints
@api.route('/images', defaults={'filename': 'filler.jpg'})
@api.route('/images/<filename>')
def image_file(filename):
    return send_from_directory('static/images', filename)



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

