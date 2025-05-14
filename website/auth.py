from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from website import db
from website.models import User, Post
from website.forms import RegistrationForm, LoginForm, UpdateAccountForm
from io import BytesIO
import os
import secrets
from flask import current_app as app
from PIL import Image



auth = Blueprint('auth', __name__, url_prefix='/auth')

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('views.dashboard'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        new_user = User(email=form.email.data, password=hashed_password, name=form.name.data)
        db.session.add(new_user)
        db.session.commit()
        flash('Your account has been created!', category='success')
        return redirect(url_for('auth.login'))
    return render_template('register.html', form=form, title='Register')

# login route
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('views.dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Login successful!', category='success')
            return redirect(url_for('views.dashboard'))
        else:
            flash('Login failed. Check your email and password.', category='error')
    return render_template('login.html', form=form, title='Login', user=current_user)

# logout route
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out!', category='success')
    return redirect(url_for('auth.login'))

# update account route
@auth.route('/update_account', methods=['GET', 'POST'])
@login_required
def update_account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.email = form.email.data
        current_user.name = form.name.data
        if form.profile_picture.data:
            picture_file = save_profile_picture(form.profile_picture.data)
            current_user.profile_picture = picture_file
        db.session.commit()
        flash('Your account has been updated!', category='success')
        return redirect(url_for('views.account'))
    elif request.method == 'GET':
        form.email.data = current_user.email
        form.name.data = current_user.name
    return render_template('update_account.html', form=form, title='Update Account')

# Function to save profile picture
def save_profile_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

# Function to delete profile picture
def delete_profile_picture(picture_file):
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_file)
    if os.path.exists(picture_path):
        os.remove(picture_path)
    return True

# Function to delete user account
@auth.route('/delete_account', methods=['POST'])
@login_required
def delete_account():
    user = User.query.get(current_user.id)
    if user:
        db.session.delete(user)
        db.session.commit()
        flash('Your account has been deleted!', category='success')
        logout_user()
        return redirect(url_for('auth.register'))
    else:
        flash('Account deletion failed.', category='error')
    return redirect(url_for('views.account'))

