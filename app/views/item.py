from app.model import Item, Category
from app.utils.utils import get_session, allowed_file, get_rand_string
from flask import Blueprint, render_template, request, redirect, url_for
from flask import current_app as app, flash

from werkzeug.utils import secure_filename

import os

session = get_session('sqlite:///catalog.db')
item = Blueprint('item',
                        __name__,
                        template_folder='templates')

@item.route('/')
@item.route('/category/<int:category_id>/items')
def getItems(category_id):
    pass

@item.route('/category/<int:category_id>/items/new', methods=['GET', 'POST'])
def createItem(category_id):
    category = session.query(Category).filter(Category.id == category_id).one()
    if request.method == 'GET':
        try:
            return render_template('item/index.html', category=category)

        except:
            raise

    if request.method == 'POST':
        try:
            params = request.form

            # create an item object from form params
            item = Item(
                type=category.name,
                name=params['name'],
                details=params['details'])

            if 'image' in request.files.keys():
                image = request.files['image']

            # save image asset and set image_name property for the item
            if image and allowed_file(image.filename, app.config):
                image_name = (get_rand_string() + '.').join([str(x) for x in secure_filename(image.filename).split('.')])
                path = os.path.join(app.config['IMAGE_FOLDER'], image_name)
                image.save(path)
                item.image_name = image_name

            # connect item to its category
            item.item_children.append(category)

            # add item to database
            session.add(item)
            session.commit()

            # send feedback to the user
            flash("%s created!" % item.name)

            return redirect(url_for("category.allCategories"))

        except:
            session.rollback()
            raise



