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