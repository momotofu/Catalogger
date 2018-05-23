from app.model import Item, Category
from app.utils.utils import get_session
from flask import Blueprint, render_template, request

session = get_session('sqlite:///catalog.db')
item = Blueprint('item',
                        __name__,
                        template_folder='templates')

@item.route('/')
@item.route('/items/<int:category_id>')
def getItems(category_id):
    pass

@item.route('/items/<int:category_id>/new', methods=['GET', 'POST'])
def createItem(category_id):
    if request.method == 'GET':
        try:
            category = session.query(Category).filter(Category.id == category_id).one()
            return render_template('item/index.html', category=category)

        except:
            raise



