使用此文档记录项目所用技术

## flask-script
使用该组件，可直接创建上下文，便于在命令行模式下对数据库操作
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
使用该组件对数据库进行操作
创建学生与课程之间的多对多关系
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

## 工厂模式创建app
做初始化是非常好用
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
## 蓝图，路由分发
```
from flask import Blueprint


admin = Blueprint('admin', __name__, url_prefix='/admin')

from . import views
```
## 程序流程
### /  首页登录
1、首页进行认证，和数据库中成员进行匹配，设置session

2、判断是否已经选课，是跳转/detail，否跳转/choose

### /choose 选课
1、通过session认证，否 --> /

2. 判断是否已经选课，是跳转/detail 是--> /detail

3.进行选课操作

### /detail

1、通过session认证，否 --> /

2、 判断是否已经选课，否跳转/choose

3、显示选课详情

## 缺点
1、未使用装饰器进行验证

2、代码过于臃肿，逻辑过于复杂
