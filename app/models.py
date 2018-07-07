from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from app import db, login, app
from flask_login import UserMixin
from hashlib import md5
from time import time
import jwt

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), index = True, unique = True)
    email = db.Column(db.String(120), index = True, unique = True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref = 'author', lazy = 'dynamic')
    entries = db.relationship('Entry', backref = 'author', lazy = 'dynamic')
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    # emotions = db.Column(db.String(140), default="")
    # thoughts = db.Column(db.String, default="")


    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_own_posts(self):
        return Post.query.filter_by(user_id = self.id).order_by(Post.timestamp.desc())

    def get_own_entries(self):
        """ Returns a Query object. To get items, use .all() """
        # Also need to filter by published boolean variable
        return Entry.query.filter_by(user_id = self.id, is_published = True).order_by(Entry.timestamp.desc())

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)

    def get_reset_password_token(self, expires_in = 600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            app.config['SECRET_KEY'], algorithm = 'HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'],
                            algorithms = ['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)

    def __repr__(self):
        return '<User {}>'.format(self.username)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    title = db.Column(db.String(140))
    slug = db.Column(db.String(140), unique = True)
    body = db.Column(db.String(140))
    is_published = db.Column(db.Boolean)
    timestamp = db.Column(db.DateTime, index = True, default = datetime.utcnow)
    sentiment = db.Column(db.String)
    keywords = db.Column(db.String)
    language = db.Column(db.String(5))

    # Metric Information 
    polarity = db.Column(db.Integer)
    subjectivity = db.Column(db.Integer)
    mood_tags = db.Column(db.String)
    word_semantics = db.Column(db.String)
    attention = db.Column(db.Integer)
    sensitivity = db.Column(db.Integer)
    pleasantness = db.Column(db.Integer)
    aptitude = db.Column(db.Integer)
    depression_factor = db.Column(db.Integer)

    def __repr__(self):
        return '<Post {}>'.format(self.body)

class Entry(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    title = db.Column(db.String(140))
    slug = db.Column(db.String(140), unique = True)
    content = db.Column(db.String)
    is_published = db.Column(db.Boolean)
    timestamp = db.Column(db.DateTime, default = datetime.utcnow)
    sentiment = db.Column(db.String)
    keywords = db.Column(db.String)
    language = db.Column(db.String(5))

    # Metric Information 
    polarity = db.Column(db.Integer)
    subjectivity = db.Column(db.Integer)
    mood_tags = db.Column(db.String)
    word_semantics = db.Column(db.String)
    attention = db.Column(db.Integer)
    sensitivity = db.Column(db.Integer)
    pleasantness = db.Column(db.Integer)
    aptitude = db.Column(db.Integer)
    depression_factor = db.Column(db.Integer)

    def __repr__(self):
        return '<Entry {}>'.format(self.content)
