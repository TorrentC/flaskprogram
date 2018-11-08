from app import create_app, db
from flask_script import Manager, Shell
from app.models import Student, User, Class

app = create_app()
manager = Manager(app)


def make_shell_context():
    return dict(app=app, db=db, User=User, Class=Class, Student=Student)


manager.add_command('shell', Shell(make_context=make_shell_context))

manager.run()