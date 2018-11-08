from . import admin
from ..models import Student
from flask import render_template, send_from_directory
from datetime import datetime
import xlrd, xlsxwriter, os


@admin.route('/')
def info():
    students = Student.query.all()
    return render_template('admin/info.html', students=students, current_time=datetime.utcnow())


@admin.route('/down')
def down():
    import os
    dirs = os.path.dirname(os.path.realpath(__name__))
    students = Student.query.all()
    workbook = xlsxwriter.Workbook('students.xlsx')
    worksheet = workbook.add_worksheet()
    row = 0
    for s in students:
        worksheet.write(row, 0, s.number)
        worksheet.write(row, 1, s.name)
        c = s.classes.all()
        worksheet.write(row, 2, c[0].name)
        worksheet.write(row, 3, c[1].name)

        row += 1
    workbook.close()
    return send_from_directory(dirs, 'students.xlsx')