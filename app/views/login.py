from flask import Blueprint, render_template, request, redirect
from flask import url_for, flash, session as login_session
from flask_login import login_required, logout_user, current_user
from flask_login import login_user

from .forms import LoginForm
from app.model import User
from app.app import session
from app.utils.utils import get_rand_string

import bcrypt

login = Blueprint('login',
                        __name__,
                        template_folder='templates')


@login.route('/signup', methods=['POST', 'GET'])
def user_signup():
    form = LoginForm()

    if request.method == 'GET':
        return render_template('login/signup.html', form=form)

    elif request.method == 'POST':
        if form.validate() == False:

            flash('All fields are required')

            return render_template('login/signup.html', form=form)

        else:
            # generate a password hash from the users' password
            pw_hash = bcrypt.hashpw(form.password.data.encode(), bcrypt.gensalt())
            email = form.email.data

            # check to make sure user doesn't already exist
            try:
                prev_user = session.query(User).filter(User.email ==
                        email).one_or_none()

                if not prev_user:
                    # create a new user
                    user = User(
                            email=email,
                            password_hash=pw_hash,
                            authenticated=True)

                    # add user to the database
                    session.add(user)
                    session.commit()

                    # store user in session
                    login_user(user, remember=True)

                    # provide the user feedback
                    flash('Welcome %s' % user.name)

                    return redirect(url_for('category.allCategories'))


                else:
                    # notify that a user has already been created with that
                    # email
                    flash('A user already exists with that email')

                    return redirect(url_for('login.user_signup'))

            except:
                session.rollback()
                raise



@login.route('/login', methods=['POST', 'GET'])
def user_login():
    form = LoginForm()

    if request.method == 'POST':
        if form.validate() == False:

            flash('All fields are required')

            return render_template('login/login.html', form=form)

        else:
            # get a reference to the user model
            user = session.query(User).filter(User.email ==
                    form.email.data).one_or_none()

            if (not user or not
                bcrypt.checkpw(
                    form.password.data.encode(),
                    user.password_hash)
                ):
                # provide user feedback
                flash('The email or password entered was not correct')

                return redirect(url_for('login.user_login'))

            else:
                user.authenticated = True

                try:
                    # update datebase
                    session.add(user)
                    session.commit()

                    # store user in session
                    login_user(user, remember=True)

                    # provide the user feedback
                    flash('Welcome back %s' % user.name)

                    return redirect(url_for('category.allCategories'))

                except:
                    session.rollback()

                    # provide the user feedback
                    flash('Could not login')

                    return redirect(url_for('login.user_login'))

    else:
        state = get_rand_string()
        login_session['state'] = state

        return render_template('login/login.html', form=form, state=state)


@login.route("/logout", methods=["GET"])
@login_required
def logout():
    user = current_user
    user.authenticated = False

    try:
        session.add(user)
        session.commit()
        logout_user()

        # provide the user feedback
        flash('Successfuly logged out!')

        return redirect(url_for('category.allCategories'))

    except:
        session.rollback()
        raise
