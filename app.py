from mimetypes import inited

from flask import Flask,session,g
import config
from exts import db,mail
from models import UserModel
from blueprints.author import bp as author_bp
from blueprints.posts import bp as exchangeposts_bp
from flask_migrate import Migrate

# blueprint:做模块化

app = Flask(__name__)
# 绑定配置文件config
app.config.from_object(config)
migrate = Migrate(app, db)
db.init_app(app)
app.register_blueprint(author_bp)
app.register_blueprint(exchangeposts_bp)
mail.init_app(app)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['DEBUG'] = True



# flask db init 一次
# flask db migrate
# flask db upgrade

# 钩子函数 before_request / before_first_request / after_request ....
# hook
@app.before_request
def my_before_request():
    user_id = session.get('user_id')
    if user_id:
        user = UserModel.query.get(user_id)
        setattr(g, 'user', user)
    else:
        setattr(g, 'user', None)

@app.context_processor
def my_context_processor():
    return {'user': g.user}


if __name__ == '__main__':
    app.run()
