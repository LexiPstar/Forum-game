import wtforms
from wtforms.validators import Email, Length, EqualTo
from exts import db
# from blueprints.author import email_captcha
from models import UserModel, EmailcaptchaModel


#验证器validators，前端提交表单是否符合要求
class RegisterForm(wtforms.Form):
    email = wtforms.StringField(validators=[Email(message='邮箱格式错误！')])
    captcha = wtforms.StringField(validators=[Length(min=6,max=6,message='验证码错误!')])
    username = wtforms.StringField(validators=[Length(min=4,max=20,message='用户名格式错误!')])
    password = wtforms.PasswordField(validators=[Length(min=6,message='')])
    password_confirm=wtforms.PasswordField(validators=[EqualTo('password',message='两次输入密码不一致')])

#自定义验证：
    # 邮箱是否注册过
    # 邮箱验证码是否错误
    # 用户名是否重复
    def validate_email(self, field):
        email = field.data
        user = UserModel.query.filter_by(email=email).first()
        if user:
            raise wtforms.ValidationError(message='该邮箱已经注册！')

    def validate_captcha(self, field):
        captcha = field.data
        email =self.email.data
        captcha_model = EmailcaptchaModel.query.filter_by(email=email,captcha=captcha).first()
        if not captcha_model:
            raise wtforms.ValidationError(message='验证码错误！')

        # else:
        #     #todo 删除已验证captcha_model
        #     db.session.delete(captcha_model)
        #     db.session.commit()

    def validate_username(self, field):
        username = field.data
        user = UserModel.query.filter_by(username=username).first()
        if user:
            raise wtforms.ValidationError(message='用户名已经存在！')


class LoginForm(wtforms.Form):
    email = wtforms.StringField(validators=[Email(message='邮箱格式错误！')])
    password = wtforms.PasswordField(validators=[Length(min=6, message='')])


class QuestionForm(wtforms.Form):
    title = wtforms.StringField(validators=[Length(min=3,max=100,message='标题字符过长')])
    content = wtforms.StringField(validators=[Length(min=10,message='内容字数过少')])