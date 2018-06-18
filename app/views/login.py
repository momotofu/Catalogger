from flask import Blueprint, render_template, request, redirect
from flask import url_for, flash, session as login_session
from flask import current_app as app
from flask_login import login_required, logout_user, current_user
from flask_login import login_user

from .forms import LoginForm
from app.model import User
from app.app import session
from app.utils.utils import get_rand_string, get_credentials_for

import bcrypt
import json
import requests
import urllib.parse as urlparse
from pdb import set_trace as bp

login = Blueprint('login',
                        __name__,
                        template_folder='templates')


@login.route('/signup', methods=['POST', 'GET'])
def user_signup():
    form = LoginForm()

    if request.method == 'GET':
        state = get_rand_string()
        login_session['state'] = state

        # populate an oauth credentials dictionary to be used for client side
        # oauth
        github_creds = get_credentials_for('oauth', 'github')
        oauth = {'github_client_id': github_creds['client_id']}

        return render_template('login/signup.html', oauth=oauth, form=form)

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
        # Todo: implement session token for security
        state = get_rand_string()
        login_session['state'] = state

        # populate an oauth credentials dictionary to be used for client side
        # oauth
        github_creds = get_credentials_for('oauth', 'github')
        oauth = {'github_client_id': github_creds['client_id']}

        return render_template('login/login.html', form=form, state=state,
                oauth=oauth)


@login.route('/logout', methods=['GET'])
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

@login.route('/ghconnect')
def githubConnect():
    state = request.args.get('state')

    # ensure state is the same
    if not state == login_session['state']:
        # provide the user feedback
        flash('failed to authenticate using github')

        return redirect(url_for('login.user_login'))

    # get githubs temporary code ...
    session_code = request.args.get('code')

    # ... and POST it back to github
    try:
        github_creds = get_credentials_for('oauth', 'github')

        payload = {
            'client_id': github_creds['client_id'],
            'client_secret': github_creds['client_secret'],
            'code': session_code,
            'accept': 'json'}

        result = urlparse.parse_qs(
            requests.get(
                'https://github.com/login/oauth/access_token',
                params=payload).text)

        if 'error' in result:
            # let developer know why oath failed
            print('%s - while trying to authenticate: ' % result['error'])

            # provide the user feedback
            flash('failed to authenticate using github')

            return redirect(url_for('login.user_login'))

        # get scope of user allowed data
        scopes = result['scope']
        has_user_email_scope = True if 'user:email' in scopes else False

        if not has_user_email_scope:
            # provide the user feedback
            flash('You must provide email access to create an account')

            return redirect(url_for('login.user_login'))


        # get access token from github oauth response
        access_token = result['access_token']
        payload = { 'access_token': access_token }

        # fetch user information
        # auth_result = requests.get('https://api.github.com/user',
            # params=payload).json()
        auth_result = {}

        # fetch user private email
        auth_result['private_emails'] = (
        requests.get('https://api.github.com/user/emails',
            params=payload).json())

        user_email = auth_result['private_emails'][0]['email']

        # get reference to user model
        user = (
            session.query(User)
            .filter(User.email == user_email)
            .one_or_none())

        if not user:
            # create a user
            return json.dumps(auth_result)

        user.authenticated = True

        # update datebase
        session.add(user)
        session.commit()

        # store user in session
        login_user(user, remember=True)

        # provide the user feedback
        flash('Welcome back %s' % user.name)

        return redirect(url_for('category.allCategories'))

    except:
        raise
        # provide the user feedback
        flash('failed to authenticate using github')

        return redirect(url_for('login.user_login'))


