from exts import db
from datetime import datetime


class UserModel(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(300), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    join_time = db.Column(db.DateTime, nullable=False, default=datetime.now)


class EmailcaptchaModel(db.Model):
    __tablename__ = 'email_captcha'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(50), nullable=False)
    captcha = db.Column(db.String(50), nullable=False)
    # used = db.Column(db.Boolean, nullable=False, default=False)


class QuestionModel(db.Model):
    __tablename__ = 'question'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text,nullable=False)
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.now)

    #外键
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    author = db.relationship(UserModel, backref='questions')


class CommentatorModel(db.Model):
    __tablename__ = 'commentator'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.now)

# 谁发布，哪个贴   外键
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#关系
    question = db.relationship(QuestionModel, backref=db.backref('commentators', order_by=create_time.desc()))
    author = db.relationship(UserModel, backref='commentators')