ʹ�ô��ĵ���¼��Ŀ���ü���

## flask-script
ʹ�ø��������ֱ�Ӵ��������ģ�������������ģʽ�¶����ݿ����
```
from app import create_app, db
from flask_script import Manager, Shell
from app.models import Student, User, Class

app = create_app()
manager = Manager(app)


def make_shell_context():
    return dict(app=app, db=db, User=User, Class=Class, Student=Student)


manager.add_command('shell', Shell(make_context=make_shell_context))

manager.run()
```
## flask_sqlalchemy
ʹ�ø���������ݿ���в���
����ѧ����γ�֮��Ķ�Զ��ϵ
```
from . import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String, unique=True)
    name = db.Column(db.String, index=True)

    def __str__(self):
        return '<User %r>' % self.name


registrations = db.Table(
    'registrations',
    db.Column('student_id', db.Integer, db.ForeignKey('students.id')),
    db.Column('class_id', db.Integer, db.ForeignKey('classes.id'))
)


class Student(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    number = db.Column(db.String)
    classes = db.relationship('Class', secondary=registrations, backref=db.backref('students', lazy='dynamic'), lazy='dynamic')

    def __str__(self):
        return '<student %r>' % self.name


class Class(db.Model):
    __tablename__ = 'classes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    capacity = db.Column(db.Integer)

    def __str__(self):
        return '<class %r>' % self.name
```

## ����ģʽ����app
����ʼ���Ƿǳ�����
```
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    moment.init_app(app)
    bootstrap.init_app(app)
    db.init_app(app)

    from .main import main
    from .admin import admin
    app.register_blueprint(main)
    app.register_blueprint(admin)

    return app
```
## ��ͼ��·�ɷַ�
```
from flask import Blueprint


admin = Blueprint('admin', __name__, url_prefix='/admin')

from . import views
```
## ��������
### /  ��ҳ��¼
1����ҳ������֤�������ݿ��г�Ա����ƥ�䣬����session

2���ж��Ƿ��Ѿ�ѡ�Σ�����ת/detail������ת/choose

### /choose ѡ��
1��ͨ��session��֤���� --> /

2. �ж��Ƿ��Ѿ�ѡ�Σ�����ת/detail ��--> /detail

3.����ѡ�β���

### /detail

1��ͨ��session��֤���� --> /

2�� �ж��Ƿ��Ѿ�ѡ�Σ�����ת/choose

3����ʾѡ������

## ȱ��
1��δʹ��װ����������֤

2���������ӷ�ף��߼����ڸ���
