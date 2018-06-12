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
    return User.query.get(user_id)


@login.route('/signup', methods=['POST', 'GET'])
def user_signup():
    pass


@login.route('/login', methods=['POST', 'GET'])
def user_login():
    form = LoginForm()

    if request.method == 'POST':
        if form.validate() == False:

            flash('All fields are required')

            return render_template('login/login.html', form=form)

        else:
            # get a reference to user model
            user = User.query.get(form.email.data)

            if user:
                if bcrypt.check_password_hash(user.password, form.password.data):
                    user.authenticated = True
                    try:
                        session.add(user)
                        session.commit()
                        login_user(user, remember=True)

                        flash('Welcome back %s' % user.name)

                        return redirect(url_for('category.allCategories'))

                    except:
                        session.rollback()
                        raise

    else:
        return render_template('login/login.html', form=form)
