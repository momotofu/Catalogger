from flask import Blueprint, render_template, request, redirect
from flask import url_for, flash
from flask_login import LoginManager
from .forms import LoginForm
from app.model import User
from app.utils.utils import get_session, get_rand_string

session = get_session('sqlite:///catalog.db')
login = Blueprint('login',
                        __name__,
                        template_folder='templates')

login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id):
    try:
        user = session.query(User).filter(User.id == user.id)
        return user
    except:
        return None


@login.route('/login', methods=['POST', 'GET'])
def user_login():
    form = LoginForm()

    if request.method == 'POST':
        if form.validate() == False:
            flash('All fields are required')
            return render_template('login/login.html', form=form)
        else:
            return redirect(url_for('category.allCategories'))
    else:
        return render_template('login/login.html', form=form)
