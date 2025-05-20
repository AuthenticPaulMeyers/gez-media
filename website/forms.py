

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField, TextAreaField , SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from flask_wtf.file import FileAllowed

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[Email()], render_kw={"placeholder": "Enter your email"})
    username = StringField('Username', validators=[Length(min=2, max=150)], render_kw={"placeholder": "Enter your username"})
    password = PasswordField('Password', validators=[Length(min=6)], render_kw={"placeholder": "Enter your password"})
    confirm_password = PasswordField('Confirm Password', validators=[EqualTo('password')], render_kw={"placeholder": "Confirm your password"})
    profile_picture = FileField('Profile Picture', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={"placeholder": "Enter your email"})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={"placeholder": "Enter your password"})
    submit = SubmitField('Login')

class UpdateAccountForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={"placeholder": "Enter your email"})
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=150)], render_kw={"placeholder": "Enter your username"})
    profile_picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    password = PasswordField('Password', validators=[Length(min=6)], render_kw={"placeholder": "Update password"})
    confirm_password = PasswordField('Confirm Password', validators=[EqualTo('password')], render_kw={"placeholder": "Confirm password"})
    submit = SubmitField('Save changes')


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=1, max=150)], render_kw={"placeholder": "Enter title"})
    content = TextAreaField('Content', validators=[DataRequired()], render_kw={"placeholder": "Paste your content here"})
    image = FileField('Upload cover photo', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    category = SelectField('Category', choices=[], validators=[DataRequired()])
    submit = SubmitField('Post')

class CategoryForm(FlaskForm):
    name = StringField('New Category', validators=[DataRequired(), Length(min=1, max=150)], render_kw={"placeholder": "Enter category name"})
    submit = SubmitField('Create Category')

    