## flask-wtf
����򵥱�
```
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length


class NameForm(FlaskForm):
    name = StringField("What's your name?", validators=[DataRequired()])
    file = FileField('file upload')
    submit = SubmitField('submit')
```
wtform֧���ֶ�����
| �ֶ�	 | ˵��|
| ------ | ------ |
|StringField|�ı��ֶ�|
|TextAreaField	|�����ı��ֶ�
|PasswordField|	�����ı��ֶ�
|HiddenField	|�����ı��ֶ�
|DateField|	�ı��ֶΣ�ֵΪ datetime.date ��ʽ
|DateTimeField	|�ı��ֶΣ�ֵdatetime.datetime ��ʽ
|IntegerField|	�ı��ֶΣ�ֵΪ����
|DecimalField	|�ı��ֶΣ�ֵΪ decimal.Decimal
|FloatField	|�ı��ֶΣ�ֵΪ������
|BooleanField	|��ѡ��ֵΪ True �� False
|RadioField	|һ�鵥ѡ��
|SelectField	|�����б�
|SelectMultipleField	|�����б���ѡ����ֵ
|FileField	|�ļ��ϴ��ֶ�
|SubmitField	|���ύ��ť
|FormField	|�ѱ���Ϊ�ֶ�Ƕ����һ����
|FieldList	|һ��ָ�����͵��ֶ�

wtform��֤����
|����|˵��
|----|----|
|Email| ��֤�����ʼ���ַ|
|EqualTo |�Ƚ������ֶε�ֵ��������Ҫ�����������������ȷ�ϵ����
|IPAddress |��֤IPv4�����ַ
|Length| ��֤�����ַ����ĳ���
|NumberRange |��֤�����ֵ�����ַ�Χ��
|Optional |������ֵʱ����������֤����
|Required| ȷ���ֶ���������
|Regexp |ʹ��������ʽ��֤����ֵ
|URL|��֤URL
|AnyOf |ȷ������ֵ�ڿ�ѡֵ�б���
|NoneOf| ȷ������ֵ���ڿ�ѡ�б���

��ģ����ʹ��
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
����ͼ������ʹ��
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
## Flash����
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

python manager.py db init �����ֿ�

python manager.py db migrate -m 'change' �����¼���ֿ⣨-m��ѧʹ�ã�

python manager.py db upgrade �������ݿ�

## ���ݿ�
ʹ��Werkzeug��������
```
>>> from werkzeug.security import generate_password_hash, check_password_hash

>>> passwd = generate_password_hash('password')
>>> check_password_hash(passwd, 'password')
True
>>> passwd
'pbkdf2:sha256:50000$sDHqvdve$bad3efcbf536aeea149cf88470f2929d5f02b8b159061b01e9310f08eb3834f3'
```
�����ݿ���Ӧ��(һ�Զ�)
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

flask-loginҪ���û�ʵ�ַ����� ��ֱ�Ӽ̳�UserMixin
```
is_active
is_authenticated
is_anonymous
 get_id  

from flask_login import UserMixin
class User(UserMixin, db.Model):pass
```
flask-login�ڹ�������������ʼ��
```
from flask_login import LoginManager

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'
login_manager.init_app(app)
```
ע���û�
```
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
```
��¼�ǳ���֤
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



  



