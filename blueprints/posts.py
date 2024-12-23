from flask import Blueprint, request, render_template,g,redirect,url_for
from .forms import QuestionForm
from  models import QuestionModel
from exts import db

bp = Blueprint('posts', __name__, url_prefix='')

@bp.route('/')
def index():
    return '首页'

@bp.route('/posts/public', methods=['GET', 'POST'])
def public_question():
    if request.method == 'GET':
        return render_template('posts.html')
    else:
        form = QuestionForm(request.form)
        if form.validate():
            title = form.title.data
            content = form.content.data
            question = QuestionModel(title=title, content=content,author=g.user)
            db.session.add(question)
            db.session.commit()
            return redirect('/')
        else:
            print(form.errors)
            return redirect(url_for('posts.public_question'))