from . import db
from werkzeug.security import generate_password_hash,check_password_hash
from . import login_manager
from flask_login import UserMixin
from . import login_manager
from datetime import datetime


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(UserMixin,db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255),index = True)
    email = db.Column(db.String(255),unique = True,index = True)
    password_hash = db.Column(db.String(255))
    bio = db.Column(db.String(255))
    subscription = db.Column(db.Boolean)
    profile_pic_path = db.Column(db.String())
    pass_secure = db.Column(db.String(255))
    date_joined = db.Column(db.DateTime, default=datetime.utcnow)

    
    diseases = db.relationship('Disease', backref='disease', lazy="dynamic")
    # comments = db.relationship('Comment', backref='user', lazy='dynamic')

    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self, password):
        self.pass_secure = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.pass_secure, password)

    def __repr__(self):
        return f'User {self.username}'


class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))

    def __repr__(self):
        return f'User {self.name}'


class Disease(db.Model):
    __tablename__ = 'diseases'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    category = db.Column(db.String())
    symptoms = db.Column(db.String())
    control = db.Column(db.String())
    approved = db.Column(db.String())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)

    comments = db.relationship('Comment', backref='disease_id', lazy='dynamic')

    def save_disease(self):
        db.session.add(self)
        db.session.commit()

    def get_disease(id):
        disease = Disease.query.filter_by(id=id).first()
        return disease



class Symptom(db.Model):
    __tablename__ ='symptoms'

    id = db.Column(db.Integer, primary_key=True)
    symptom = db.Column(db.String())
   

    def save_symptom(self):
        db.session.add(self)
        db.session.commit()
        
    def get_symptom(id):
        symptom = Symptom.query.filter_by(id=id).first()
        return symptom


class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(1000))
    username = db.Column(db.String(1000))

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    disease = db.Column(db.Integer, db.ForeignKey('diseases.id'))

    def save_comment(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_comments(cls, disease):
        comments = Comment.query.filter_by(disease=disease.id).all()
        return comments



class Subscribe(db.Model):
    __tablename__ = 'subscribe'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255),unique = True,index = True, nullable=False)

def __repr__(self):
        return f'{self.email}'
    # def save_subscribe(self):
    #     db.session.add(self)
    #     db.session.commit()
    #     return subscribe
   


# class Quotes:
#     '''
#     News class to define quote Objects
#     '''

#     def __init__(self,id,author,quote):
#         self.id = id
#         self.author = author
#         self.quote = quote
      



