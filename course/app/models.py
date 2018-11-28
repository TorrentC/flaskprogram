from . import db, login_manager
from flask_login import UserMixin


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String, unique=True)
    name = db.Column(db.String, index=True)

    def __repr__(self):
        return '<User %r>' % self.name


registrations = db.Table(
    'registrations',
    db.Column('student_id', db.Integer, db.ForeignKey('students.id')),
    db.Column('class_id', db.Integer, db.ForeignKey('classes.id'))
)


class Student(UserMixin, db.Model):
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    number = db.Column(db.String)
    checked = db.Column(db.Boolean, default=False)
    classes = db.relationship('Class', secondary=registrations, backref=db.backref('students', lazy='dynamic'), lazy='dynamic')

    def __repr__(self):
        return '<student %r>' % self.name


class Class(db.Model):
    __tablename__ = 'classes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    capacity = db.Column(db.Integer)

    def __repr__(self):
        return '<class %r>' % self.name


@login_manager.user_loader
def load_user(user_id):
    return Student.query.get(user_id)