from flask import render_template, url_for, flash, redirect, request, Blueprint, send_file
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from website import db
from website.models import Post, User, Category
from website.forms import PostForm, CategoryForm
from werkzeug.utils import secure_filename
from io import BytesIO

# create a blueprint for the views routes
views = Blueprint('views', __name__, url_prefix='/gezmedia-blog')

# create a route for the home page
@views.route('/')
@views.route('/home')
def home():
    return render_template('home.html', title='Home')

# create a route for the dashboard page
@views.route('/dashboard')
@login_required
def dashboard():
    posts = Post.query.filter_by(user_id=current_user.id).all()
    latest_posts = Post.query.filter_by(user_id=current_user.id).order_by(Post.date_posted.desc()).limit(5).all()
    total_posts = len(posts)
    total_users = User.query.count()
    total_categories = Category.query.count()

    return render_template('dashboard.html', title='Dashboard', user=current_user, posts=posts, total_posts=total_posts, total_users=total_users, latest_posts=latest_posts, total_categories=total_categories)

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
    post = Post.query.filter_by(id=post_id, user_id=current_user.id).first()

    # get the post and increment the views
    if post:
        post.views += 1
        db.session.commit()
    else:
        flash('Post not found!', category='error')
        return redirect(url_for('views.blog'))

    return render_template('post.html', title=post.title, post=post)


# create a route for the create post page
@views.route('/create_post', methods=['GET', 'POST'])
@login_required
def create_post():
    form = PostForm()
    category = Category.query.all()
    form.category.choices = [(c.id, c.name) for c in category]

    if form.validate_on_submit():
        image = form.image.data
        title = form.title.data
        content = form.content.data
        category_id = form.category.data

        if image:
            image_mimetype = image.mimetype
            image_filename = secure_filename(image.filename)
            image_data = image.read()
            post = Post(title=title, content=content, author=current_user, category_id=category_id, image_filename=image_filename, image_mimetype=image_mimetype, image_data=image_data)
           
            db.session.add(post)
            db.session.commit()
            flash('Your post has been created!', category='success')
            return redirect(url_for('views.dashboard'))
    return render_template('create_post.html', title='Create Post', form=form)

# create a route for the edit post page
@views.route('/edit_post/<int:post_id>', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)

    form = PostForm(obj=post)
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', category='success')
        return redirect(url_for('views.post', post_id=post.id))
    return render_template('edit_post.html', title='Edit Post', form=form, post=post)

# create a route for the delete post page
@views.route('/delete_post/<int:post_id>', methods=['POST', 'GET'])
@login_required
def delete_post(post_id):
    post = Post.query.filter_by(id=post_id, user_id=current_user.id).first()

    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', category='success')
    return redirect(url_for('views.dashboard'))

# route to read images from the database
@views.route('/image/<int:post_id>')
def post_image(post_id):
    post = Post.query.filter_by(id=post_id).first()
    # Check if the post exists and has a profile picture
    if post and post.image_data:
        mimetype = post.image_mimetype or 'image/png'
        download_name = post.image_filename
        return send_file(BytesIO(post.image_data), mimetype=mimetype, download_name=download_name)
    return "Image not found!", 404
