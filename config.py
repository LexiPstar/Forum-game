
SECRET_KEY = 'asfdagsgaysgfysafsyufas;lf'

HOSTNAME = '127.0.0.1'
PORT = 3306
DEBUG = True
DATABASE = 'liuligongcheng'
USERNAME = 'root'
PASSWORD = '5739'
DB_URI='mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8mb4'.format(USERNAME,PASSWORD,HOSTNAME,PORT,DATABASE)
SQLALCHEMY_DATABASE_URI = DB_URI

#邮箱配置
MAIL_SERVER = 'smtp.qq.com'
MAIL_PORT = 465
MAIL_USERNAME = '@email.com'
MAIL_PASSWORD = 'tzqutiruxaaujjhh'
MAIL_USE_SSL = True
MAIL_DEFAULT_SENDER = '@email.com'