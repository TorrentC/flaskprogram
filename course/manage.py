from app import create_app, db
from flask_script import Manager, Shell
from app.models import Student, User, Class
from flask_migrate import Migrate, MigrateCommand

app = create_app()
manager = Manager(app)

migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)


def make_shell_context():
    return dict(app=app, db=db, User=User, Class=Class, Student=Student)


manager.add_command('shell', Shell(make_context=make_shell_context))

manager.run()

# import xlrd, xlsxwriter, os
#
#
# workbook = xlrd.open_workbook('16.xls')
# worksheet = workbook.sheets()[0]
# print(worksheet.nrows)
# for i in range(2, worksheet.nrows):
#     result = worksheet.row_values(i)
#     print(result[0], result[1])
#     u = User(number=result[0], name=result[1])
#     db.session.add(u)
#     # print(result)
# db.session.commit()


