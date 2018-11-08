from functools import wraps
from flask import session, flash, redirect


def required(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            info = session.get('info')
            if info is None:
                flash('你必需先登录！！！')
                return redirect('main.login')
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def login_required(f):
    return required(1)(f)


