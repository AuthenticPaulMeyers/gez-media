from flask import render_template, url_for, flash, redirect, request, Blueprint, send_file, session
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from website import db
from website.models import Post, User, Category
from website.forms import PostForm, CategoryForm
from werkzeug.utils import secure_filename
from io import BytesIO
from sqlalchemy import func

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
    latest_posts = Post.query.filter_by(user_id=current_user.id).order_by(Post.date_posted.desc()).limit(3).all()
    total_posts = len(posts)
    total_categories = Category.query.count()
    total_views = db.session.query(func.sum(Post.views)).scalar()

    return render_template('dashboard.html', title='Dashboard', user=current_user, posts=posts, total_posts=total_posts, latest_posts=latest_posts, total_categories=total_categories, total_views=total_views)

# create a route for the about page
@views.route('/about')
def about():
    return render_template('about.html', title='About')

# create a route for the blog page
@views.route('/blog')
def blog():
    posts = Post.query.all()
     # get latest posts
    latest_posts = Post.query.order_by(Post.date_posted.desc()).limit(5).all()

    # get categories
    categories = Category.query.all()
    # get the most viewd posts
    popular_posts = Post.query.order_by(Post.views.desc()).limit(5).all()
    return render_template('blog.html', title='Blog', posts=posts, latest_posts=latest_posts, categories=categories, popular_posts=popular_posts)

# create a route for the post page
@views.route('/post/<int:post_id>')
def post(post_id):
    post = Post.query.filter_by(id=post_id, user_id=current_user.id).first()

    # get similar posts
    similar_posts = Post.query.filter(Post.category_id == post.category_id, Post.id != post.id).order_by(func.random()).limit(2).all() if post else []

    # get the post and increment the views
    if post:
        # Use session to track viewed posts
        viewed = session.get('viewed_posts', [])

        if post_id not in viewed:
            post.views += 1
            db.session.commit()
            viewed.append(post_id)
            session['viewed_posts'] = viewed
    else:
        flash('Post not found!', category='error')
        return redirect(url_for('views.blog'))

    return render_template('post.html', title=post.title, post=post, similar_posts=similar_posts, user=current_user)


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
    post = Post.query.filter_by(id=post_id, user_id=current_user.id).first()
    if not post:
        flash('Post not found!', category='error')
        return redirect(url_for('views.dashboard'))
    


    form = PostForm(obj=post)
    category = Category.query.all()
    form.category.choices = [(c.id, c.name) for c in category]

    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', category='success')
        return redirect(url_for('views.dashboard', post_id=post.id))
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


# category routes
@views.route('/create_category', methods=['GET', 'POST'])
@login_required
def create_category():
    form = CategoryForm()
    if form.validate_on_submit():
        name = form.name.data
        category = Category(name=name)
        db.session.add(category)
        db.session.commit()
        flash('Your category has been created!', category='success')
        return redirect(url_for('views.dashboard'))
    return render_template('create_category.html', title='Create Category', form=form)

