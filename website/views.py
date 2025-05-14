from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from website import db
from website.models import Post
from website.forms import PostForm


# create a blueprint for the views routes
views = Blueprint('views', __name__, url_prefix='/views')

# create a route for the home page
@views.route('/')
@views.route('/home')
def home():
    return render_template('home.html', title='Home')

# create a route for the dashboard page
@views.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', title='Dashboard', user=current_user)

# create a route for the about page
@views.route('/about')
def about():
    return render_template('about.html', title='About')

# create a route for the blog page
@views.route('/blog')
def blog():
    posts = Post.query.all()
    return render_template('blog.html', title='Blog', posts=posts)

# create a route for the post page
@views.route('/post/<int:post_id>')
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)

# create a route for the create post page
@views.route('/create_post', methods=['GET', 'POST'])
@login_required
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', category='success')
        return redirect(url_for('views.blog'))
    return render_template('create_post.html', title='Create Post', form=form)

# create a route for the edit post page
@views.route('/edit_post/<int:post_id>', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        flash('You are not authorized to edit this post.', category='error')
        return redirect(url_for('views.blog'))
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', category='success')
        return redirect(url_for('views.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('edit_post.html', title='Edit Post', form=form, post=post)

# create a route for the delete post page
@views.route('/delete_post/<int:post_id>', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        flash('You are not authorized to delete this post.', category='error')
        return redirect(url_for('views.blog'))
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', category='success')
    return redirect(url_for('views.blog'))
