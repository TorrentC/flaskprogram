from . import main
from flask import render_template, flash, redirect, url_for, session
from datetime import datetime
from .forms import LoginForm, ChooseForm
from ..models import User, Student, Class
from wtforms import BooleanField, SubmitField
from flask_login import login_user, current_user, login_required
from .. import db


@main.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        number = form.number.data
        name = form.name.data
        # 和users表进行匹配
        user = User.query.filter_by(number=number, name=name).first()
        if user is None:
            flash('学号或姓名错误！！！')
            return redirect(url_for('.login'))

        # 检测用户是否第一次登录
        student = Student.query.filter_by(number=number, name=name).first()
        if student is None:
            student = Student(number=number, name=name)
            db.session.add(student)
            student = Student.query.filter_by(number=number, name=name).first()

        login_user(student)
        # 第一次登录，写入students表，进行选课操作。
        if current_user.checked:
            return redirect(url_for('.detail'))
        else:
            return redirect(url_for('.choose'))

    return render_template('main/index.html', current_time=datetime.utcnow(), form=form)


@main.route('/choose', methods=['GET', 'POST'])
@login_required
def choose():

    # 判断学生是否已选课, 选过直接跳到detail中
    if current_user.checked:
        return redirect(url_for('.detail'))

    # 使用setter从classes表中动态设置form字段, (和学生选课数对比，动态显示选项)
    classes = Class.query.all()
    for c in classes:
        if c.students.count() < c.capacity:
            setattr(ChooseForm, c.name, BooleanField(c.name))
    setattr(ChooseForm, 'submit', SubmitField('提交'))
    form = ChooseForm()

    # 获取form中的数据并判断是否符合条件
    if form.validate_on_submit():

        # 判断用户勾选总数，并加以限制
        total = sum([getattr(getattr(form, c.name), 'data') for c in classes if c.students.count() < c.capacity])
        if total != 2:
            flash('you only choose tow!')
            return redirect(url_for('main.choose'))

        # 获取表单字段名称和数值
        for c in classes:
            if c.students.count() < c.capacity:
                res = getattr(form, c.name)
                name = getattr(res, 'name')
                value = getattr(res, 'data')

                # 从classes表中选出表单中勾选的数据
                if value:
                    c_obj = Class.query.filter_by(name=name).first()
                    current_user.classes.append(c_obj)
        # 设置表单填写标志
        current_user.checked = True
        return redirect(url_for('.detail'))

    return render_template('main/choose.html', number=current_user.number, name=current_user.name, form=form, current_time=datetime.utcnow(), classes=classes)


@main.route('/detail')
@login_required
def detail():

    # 判断学生是否已选课, 没有选则跳到choose中
    if not current_user.checked:
        return redirect(url_for('.choose'))
    return render_template('main/detail.html', student=current_user, current_time=datetime.utcnow())

