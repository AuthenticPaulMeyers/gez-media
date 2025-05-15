from flask import render_template, url_for, flash, redirect, request, Blueprint, send_file, request
from flask_login import login_user, current_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from website import db
from website.models import User
from website.forms import RegistrationForm, LoginForm, UpdateAccountForm
from io import BytesIO
from flask import current_app as app
from werkzeug.utils import secure_filename

auth = Blueprint('auth', __name__, url_prefix='/auth')

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('views.dashboard'))
    form = RegistrationForm()
    user_email = User.query.filter_by(email=form.email.data).first()
    
    if user_email:
        flash('Email already exist. Please try a different email', category='error')
        return redirect(url_for('auth.register'))

    if request.method == 'POST':
        hashed_password = generate_password_hash(form.password.data)
        image = form.profile_picture.data
        email = form.email.data
        name = form.username.data
        if image:
            image_mimetype=image.mimetype
            image_filename = secure_filename(image.filename)
            image_data = image.read() # Read image in binary data

            new_user = User(email=email, password=hashed_password, name=name, profile_picture=image_data, image_filename=image_filename, image_mimetype=image_mimetype)
            db.session.add(new_user)
            db.session.commit()
            flash('Account created successfully!', category='success')
            return redirect(url_for('auth.login'))
        flash('Please upload a valid image file.', category='error')
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
            image = form.profile_picture.data
            image_mimetype = image.mimetype
            image_filename = secure_filename(image.filename)
            image_data = image.read()
            current_user.image_mimetype = image_mimetype
            current_user.image_filename = image_filename
            current_user.profile_picture = image_data
        db.session.commit()
        flash('Your account has been updated!', category='success')
        return redirect(url_for('views.account'))
    elif request.method == 'GET':
        form.email.data = current_user.email
        form.name.data = current_user.name
        form.profile_picture.data = current_user.profile_picture

    return render_template('update_account.html', form=form, title='Update Account')

@auth.route('/profile_picture/<int:user_id>')
def profile_picture(user_id):
    user = User.query.filter_by(id=user_id).first()

    if user and user.profile_picture:
        mimetype = user.image_mimetype or 'image/png'
        download_name = user.image_filename
        return send_file(BytesIO(user.profile_picture), mimetype=mimetype, download_name=download_name)
    return "Image not found!", 404

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

