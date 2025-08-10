from flask import render_template, url_for, flash, redirect, request, Blueprint, send_file, session
from flask_login import current_user, login_required
from website import db
from website.models import Post, Category
from website.forms import PostForm, CategoryForm
from werkzeug.utils import secure_filename
from io import BytesIO
from sqlalchemy import func

# create a blueprint for the views routes
views = Blueprint('views', __name__, url_prefix='/v1.0')

# create a route for the home page
@views.route('/')
@views.route('/index')
def index():
    # get the latest posts
    latest_articles = Post.query.order_by(Post.date_posted.desc()).limit(3).all()
    return render_template('index.html', latest_articles=latest_articles)

# get all the posts
@views.route('/posts')
@login_required
def posts():
    posts = Post.query.filter_by(user_id=current_user.id).all()
    return render_template('all_posts.html', title='Posts', posts=posts, user=current_user) 

# create a route for the dashboard page
@views.route('/dashboard')
@login_required
def dashboard():
    posts = Post.query.filter_by(user_id=current_user.id).all()
    latest_posts = Post.query.filter_by(user_id=current_user.id).order_by(Post.date_posted.desc()).limit(3).all()
    total_posts = len(posts)
    total_categories = Category.query.count()
    total_views = db.session.query(func.sum(Post.views)).filter_by(user_id=current_user.id).scalar()

    return render_template('dashboard.html', title='Dashboard', user=current_user, posts=posts, total_posts=total_posts, latest_posts=latest_posts, total_categories=total_categories, total_views=total_views)

# create a route for the about page
@views.route('/about')
def about():
    return render_template('about.html', title='About')

# create a route for the blog page
@views.route('/blog')
def blog():
    posts = Post.query.all()

    # get categories
    categories = Category.query.all()
    # get the most viewd posts
    popular_posts = Post.query.order_by(Post.views.desc()).limit(5).all()
    return render_template('blog.html', title='Blog', posts=posts, categories=categories, popular_posts=popular_posts)

# create a route for the post page
@views.route('/post/<int:post_id>')
def post(post_id):
    post = Post.query.filter_by(id=post_id).first()
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

    if form.validate_on_submit() or request.method == 'POST':
        image = form.image.data
        title = form.title.data
        content = request.form['content']
        category_id = form.category.data

        if image:
            image_mimetype = image.mimetype
            image_filename = secure_filename(image.filename)
            image_data = image.read()
            post = Post(title=title, content=content, author=current_user, category_id=category_id, image_filename=image_filename, image_mimetype=image_mimetype, image_data=image_data)
           
            db.session.add(post)
            db.session.commit()
            flash('Your post has been created!', category='success')
            return redirect(url_for('views.posts'))
    return render_template('create_post.html', title='Create Post', form=form, user=current_user)

# create a route for the edit post page
@views.route('/edit_post/<int:post_id>', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    post = Post.query.filter_by(id=post_id, user_id=current_user.id).first()
    if not post:
        flash('Post not found!', category='error')
        return redirect(url_for('views.dashboard'))
    
    form = PostForm()
    category = Category.query.all()
    form.category.choices = [(c.id, c.name) for c in category]

    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', category='success')
        return redirect(url_for('views.dashboard', post_id=post.id))
    else:
        form.title.data = post.title
        form.content.value = post.content
        form.category.data = post.category_id
    return render_template('edit_post.html', title='Edit Post', form=form, post=post, user=current_user)

# create a route for the delete post page
@views.route('/delete_post/<int:post_id>', methods=['POST', 'GET'])
@login_required
def delete_post(post_id):

    if post:
        post = Post.query.filter_by(id=post_id, user_id=current_user.id).first()

        db.session.delete(post)
        db.session.commit()
        flash('Your post has been deleted!', category='success')
        return redirect(url_for('views.dashboard'))
    flash('Post not found!', category='error')
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

# category route
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
        return redirect(url_for('views.create_category'))
    # get all categories
    categories = Category.query.all()
    return render_template('create_category.html', title='Create Category', form=form, user=current_user, categories=categories)

# delete category route
@views.route('/delete_category/<int:cat_id>', methods=['POST', 'GET'])
def delete_category(cat_id):
    # Check if the user is logged in
    category = Category.query.filter_by(id=cat_id).first()
    if not category:
        flash('Category not found!', category='error')
        return redirect(url_for('views.create_category'))
    
    # Check if the category is used in any posts
    posts = Post.query.filter_by(category_id=cat_id).all()
    if posts:
        flash('Cannot delete category. It is used in one or more posts.', category='error')
        return redirect(url_for('views.create_category'))

    db.session.delete(category)
    db.session.commit()
    flash('Your category has been deleted!', category='success')
    return redirect(url_for('views.create_category'))

# create a route for the reviews page
@views.route('/reviews')
def reviews():
    return render_template('reviews.html', title='Reviews')
