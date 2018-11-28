## flask-login

flask-login要求用户实现方法， 可直接继承UserMixin
```
is_active
is_authenticated
is_anonymous
 get_id  

from flask_login import UserMixin
class User(UserMixin, db.Model):pass
```
flask-login在工厂函数中做初始化
```
from flask_login import LoginManager

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'
login_manager.init_app(app)
```
注册用户
```
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
```
登录登出认证
```
from . import auth
from flask import render_template, flash, redirect, url_for, session, request
from datetime import datetime
from .forms import LoginForm
from flask_login import login_user, logout_user
from ..models import User


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            flash('login success')
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('Invalid username or password')
    return render_template('auth/index.html', current_time=datetime.utcnow(), form=form)


@auth.route('/logout')
def logout():
    logout_user()
    flash('you have already logged out')
    return redirect(url_for('main.index'))

@main.route('/admin123')
@login_required
def admin():
pass
```
