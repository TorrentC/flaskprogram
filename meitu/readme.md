## flask-wtf
定义简单表单
```
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length


class NameForm(FlaskForm):
    name = StringField("What's your name?", validators=[DataRequired()])
    file = FileField('file upload')
    submit = SubmitField('submit')
```
wtform支持字段类型
| 字段	 | 说明|
| ------ | ------ |
|StringField|文本字段|
|TextAreaField	|多行文本字段
|PasswordField|	密码文本字段
|HiddenField	|隐藏文本字段
|DateField|	文本字段，值为 datetime.date 格式
|DateTimeField	|文本字段，值datetime.datetime 格式
|IntegerField|	文本字段，值为整数
|DecimalField	|文本字段，值为 decimal.Decimal
|FloatField	|文本字段，值为浮点数
|BooleanField	|复选框，值为 True 和 False
|RadioField	|一组单选框
|SelectField	|下拉列表
|SelectMultipleField	|下拉列表，可选择多个值
|FileField	|文件上传字段
|SubmitField	|表单提交按钮
|FormField	|把表单作为字段嵌入另一个表单
|FieldList	|一组指定类型的字段

wtform验证函数
|函数|说明
|----|----|
|Email| 验证电子邮件地址|
|EqualTo |比较两个字段的值，常用于要求输入两次密码进行确认的情况
|IPAddress |验证IPv4网络地址
|Length| 验证输入字符串的长度
|NumberRange |验证输入的值在数字范围内
|Optional |无输入值时跳过其他验证函数
|Required| 确保字段中有数据
|Regexp |使用正则表达式验证输入值
|URL|验证URL
|AnyOf |确保输入值在可选值列表中
|NoneOf| 确保输入值不在可选列表中

在模板中使用
```
<form action="" method="post" role="form">
                {{ form.hidden_tag() }}
                <div class="form-group">
                {{ form.name.label }}
                {{ form.name(class='form-control') }}
                </div>
                {{ form.submit() }}
</form>

{% import 'bootstrap/wtf.html' as wtf %}
{{ wtf.quick_form(form) }}
```
在视图函数中使用
```
@app.route('/', methods=['GET', 'POST'])
def hello():
    name = session.get('name')
    form = NameForm()
    if form.validate_on_submit():
        name = form.name.data
        file = request.files.get('file')
        file.save(file.filename)
        session['name'] = name
        form.name.data = ''
        return redirect(url_for('hello'))
    return render_template('index.html', name=name, form=form, current_time=datetime.utcnow())
```
## Flash闪现
```
{% for message in get_flashed_messages() %}
  <div class="alert alert-warning">
   <a href="#" class="close" data-dismiss="alert">
                        &times;
    </a>
                    {{ message }}
   </div>
 {% endfor %}

```
## flask-migrate
```
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

```

python manager.py db init 创建仓库

python manager.py db migrate -m 'change' 将更新加入仓库（-m必学使用）

python manager.py db upgrade 更新数据库

## 数据库
使用Werkzeug加密密码
```
>>> from werkzeug.security import generate_password_hash, check_password_hash

>>> passwd = generate_password_hash('password')
>>> check_password_hash(passwd, 'password')
True
>>> passwd
'pbkdf2:sha256:50000$sDHqvdve$bad3efcbf536aeea149cf88470f2929d5f02b8b159061b01e9310f08eb3834f3'
```
在数据库中应用(一对多)
```
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    @property
    def password(self):
        raise AttributeError('password is not readable')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __str__(self):
        return '<User %r>' % self.username

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role')
```

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



  



