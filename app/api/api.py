from flask import Blueprint, send_from_directory
from app.utils.utils import get_session

session = get_session('sqlite:///catalog.db')
api = Blueprint('api',
                        __name__,
                        template_folder='templates')


# API endpoints
@api.route('/images', defaults={'filename': 'filler.jpg'})
@api.route('/images/<filename>')
def image_file(filename):
    return send_from_directory('static/images', filename)

