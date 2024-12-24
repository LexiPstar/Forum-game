import random
import string
from flask import Blueprint, render_template, jsonify, request, redirect, url_for, session
from flask_mail import Message

from exts import mail, db
from models import EmailcaptchaModel
from .forms import RegisterForm, LoginForm
from models import UserModel
from werkzeug.security import generate_password_hash, check_password_hash

bp = Blueprint('author', __name__, url_prefix='/author')


@bp.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        form = LoginForm(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            user = UserModel.query.filter_by(email=email).first()
            if not user:
                print('邮箱未注册')
                return redirect(url_for('author.login'))
            if check_password_hash(user.password, password):
                # cookie 只适合储存少量数据
                # cookie 一般用来存放登录授权数据
                # flask中的session 是加密存储在cookie中的
                session['user_id'] = user.id
                return redirect(url_for('posts.index'))
            else:
                print('用户名或密码输入错误！')
                return redirect(url_for('author.login'))
        else:
            print(form.errors)
            return redirect(url_for('author.login'))


# GET:服务器获取数据
# POST:将客户端数据提交服务器
@bp.route('/register', methods=['GET', 'POST'])
def register(username=None, email=None):
    if request.method == 'GET':
        return render_template("register.html")
    else:
        # 验证用户提交表单是否正确
        # 表单验证:flask wtforms
        form = RegisterForm(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            username = form.username.data
            user = UserModel(username=username, email=email, password=generate_password_hash(password))
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('author.login'))
        else:
            print(form.errors)
            return redirect(url_for('author.register'))


# 没有明确methods，默认是'GET'
@bp.route('/captcha/email')
def email_captcha():
    email = request.args.get('email')
    if not email:
        return jsonify({'code': 400, 'message': '邮箱不能为空', 'data': None})
    # 检查邮箱格式
    if '@' not in email or '.' not in email:
        return jsonify({'code': 400, 'message': '邮箱格式不正确', 'data': None})
    # 生成6位数字验证码
    source = string.digits
    captcha = ''.join(random.choices(source, k=6))
    # 创建邮件消息
    message = Message(subject='琉璃攻城', recipients=[email], body=f"您的邮箱注册验证码：{captcha}")
    try:
        mail.send(message)
    except Exception as e:
        return jsonify({'code': 500, 'message': f'邮件发送失败: {str(e)}', 'data': None})
    # 检查该邮箱是否已有验证码记录，若有则更新
    existing_record = EmailcaptchaModel.query.filter_by(email=email).first()
    if existing_record:
        existing_record.captcha = captcha  # 更新验证码
    else:
        email_captcha = EmailcaptchaModel(email=email, captcha=captcha)
        db.session.add(email_captcha)
    try:
        db.session.commit()
        return jsonify({'code': 200, 'message': '验证码已发送', 'data': None})
    except Exception as e:
        db.session.rollback()  # 如果提交失败，回滚
        return jsonify({'code': 500, 'message': f'数据库操作失败: {str(e)}', 'data': None})


@bp.route('/logout')
def logout():
    session.pop('user_id', None)  # 清除用户 ID
    session.clear()  # 清除会话数据
    return redirect(url_for('posts.index'))  # 重定向到首页
