from flask import Blueprint, render_template
from app.utils.utils import get_session, get_rand_string

session = get_session('sqlite:///catalog.db')
login = Blueprint('login',
                        __name__,
                        template_folder='templates')


@login.route('/login')
def user_login():
    """
    1. Create a state token to prevent request forgery
    and store it in the session for later validation.

    2. Render user login page.
    """

    state = get_rand_string()
    login_session['state'] = state

    return render_template('login/login.html', state=state)
