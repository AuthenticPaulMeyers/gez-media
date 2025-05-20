from flask_login import UserMixin
from website import db


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150), nullable=False)
    name = db.Column(db.String(150), nullable=False)
    profile_picture = db.Column(db.String(150), default='default.jpg')
    image_filename = db.Column(db.String(100))
    image_mimetype = db.Column(db.String(50)) 
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.id}')"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150))
    content = db.Column(db.Text)
    date_posted = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    image_filename = db.Column(db.String(100))
    image_mimetype = db.Column(db.String(50))
    image_data = db.Column(db.LargeBinary)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    views = db.Column(db.Integer, default=0)
    likes = db.Column(db.Integer, default=0)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.id}')"

# category model
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True)
    posts = db.relationship('Post', backref='category', lazy=True)
    def __repr__(self):
        return f"Category('{self.id}')"
