from app import create_app, db
from flask_script import Manager, Shell
from app.models import Image, Theme
from flask_migrate import MigrateCommand, Migrate


app = create_app()
manager = Manager(app)

migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db, Image=Image, Theme=Theme)


manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

manager.run()