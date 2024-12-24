from flask import Blueprint, request, render_template, g, redirect, url_for

import app
from .forms import QuestionForm, CommentForm
from models import QuestionModel, CommentatorModel
from exts import db
from decorators import login_required

bp = Blueprint('posts', __name__, url_prefix='', static_folder='static')


@bp.route('/')
def index():
    questions = QuestionModel.query.order_by(QuestionModel.create_time.desc()).all()
    return render_template('index.html', questions=questions)


@bp.route('/posts/public', methods=['GET', 'POST'])
@login_required
def public_question():
    if request.method == 'GET':
        form = QuestionForm()
        return render_template('posts.html', form=form)
    else:
        form = QuestionForm(request.form)
        if form.validate():
            title = form.title.data
            content = form.content.data
            question = QuestionModel(title=title, content=content, author=g.user)
            db.session.add(question)
            db.session.commit()
            return redirect('/')
        else:
            print(form.errors)
            return redirect(url_for('posts.public_question', form=form))


@bp.route('/posts/detail/<int:post_id>')
def post_detail(post_id):
    question = QuestionModel.query.get(post_id)
    return render_template('detail.html', question=question)


# @bp.route('commented/public',methods=['POST'])
@bp.post('/commented/public')
@login_required
def comment_public():
    form = CommentForm(request.form)
    if form.validate():
        content = form.content.data
        question_id = form.question_id.data
        commentator = CommentatorModel(content=content, question_id=question_id, author_id=g.user.id)
        db.session.add(commentator)
        db.session.commit()
        return redirect(url_for('posts.post_detail', post_id=question_id))
    else:
        print(form.errors)
        return redirect(url_for('posts.post_detail', post_id=request.form.get('question_id')))
