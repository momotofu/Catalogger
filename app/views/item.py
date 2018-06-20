from app.model import Item, Category
from app.utils.utils import allowed_file, get_rand_string
from app.app import session
from flask import Blueprint, render_template, request, redirect, url_for
from flask import current_app as app, flash
from flask_login import current_user

from werkzeug.utils import secure_filename

import os
import json

item = Blueprint('item',
                        __name__,
                        template_folder='templates')

@item.route('/')
@item.route('/category/<int:category_id>/items')
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


@item.route('/category/<int:category_id>/items/new', methods=['GET', 'POST'])
def createItem(category_id):
    # grab a reference to the category model
    category = session.query(Category).filter(Category.id == category_id).one()

    # render the item creation form
    if request.method == 'GET':
        return render_template('item/index.html', category=category)

    if request.method == 'POST':
        try:
            params = request.form

            # create an item object from form params
            item = Item( type=category.name, name=params['name'],
                details=params['details'])

            # attach a user to an item
            if current_user.is_authenticated:
                item.user_id = current_user.id

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

            return redirect(url_for(
                "category.allCategories",
                current_category_id=category_id))

        except:
            session.rollback()
            raise


@item.route('/category/<int:category_id>/items/<int:item_id>/edit',
methods=['GET', 'POST'])
def editItem(category_id, item_id):
    # grab a reference to the category and item models
    category = session.query(Category).filter(Category.id == category_id).one()
    item = session.query(Item).filter(Item.id == item_id).one()

    # restrict access if item doesn't belong to user
    if (not current_user.is_authenticated and item.user_id
        or (current_user.is_authenticated and
            not current_user.id == item.user_id)):

        # send feedback to the user
        flash('You do not have permission to edit that item')

        return redirect(url_for(
            'category.allCategories',
            current_category_id=category_id))

    if request.method == 'GET':
        # serve up edit form
        return render_template('item/edit.html', item=item, category=category)

    if request.method == 'POST':
        try:
            params = request.form

            # update item model from form params
            item.name = params['name'] if len(params['name']) > 0 else item.name
            item.details = params['details'] if len(params['details']) > 0 else item.details

            image = request.files['image'] if 'image' in request.files.keys() else None

            # save image asset and set image_name property for the item
            if image and image.filename != item.image_name and allowed_file(image.filename, app.config):
                image_name = (get_rand_string() + '.').join([str(x) for x in secure_filename(image.filename).split('.')])
                path = os.path.join(app.config['IMAGE_FOLDER'], image_name)
                image.save(path)
                item.image_name = image_name

            # update item in the database
            session.add(item)
            session.commit()

            # send feedback to the user
            flash("%s updated!" % item.name)

            return redirect(url_for(
                "category.allCategories",
                current_category_id=category_id))

        except:
            session.rollback()
            raise


@item.route('/category/<int:category_id>/items/<int:item_id>/delete',
methods=['POST'])
def deleteItem(category_id, item_id):
    # grab a reference to the category and item models
    item = session.query(Item).filter(Item.id == item_id).one()
    category = session.query(Category).filter(Category.id == category_id).one()

    # restrict access if item doesn't belong to user
    if (not current_user.is_authenticated and item.user_id
        or (current_user.is_authenticated and
            not current_user.id == item.user_id)):

        # send feedback to the user
        flash('You do not have permission to delete that item')

        return redirect(url_for(
            'category.allCategories',
            current_category_id=category_id))

    try:
        # remove category from item.
        item.item_children.remove(category)

        # if item doesn't have any categories then delete item from the database
        if len(item.item_children) == 0:
            session.delete(item)

        # update the database
        session.commit()

        return json.dumps({'name':item.name, 'success':True}), 200, {'ContentType':'application/json'}

    except:
        session.rollback()
        raise

