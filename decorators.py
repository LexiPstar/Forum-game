from functools import wraps
from flask import g, redirect, url_for


def login_required(func):
    @wraps(func)
    def inner(*args, **kwargs):
        if not g.user:  # 判断用户是否存在
            return redirect(url_for('author.login'))  # 如果没有登录，重定向到登录页面
        return func(*args, **kwargs)
    return inner

