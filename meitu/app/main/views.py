from . import main
from flask import render_template, request, jsonify, url_for
from datetime import datetime
from ..models import Image, Theme
from sqlalchemy.sql.expression import func


@main.route('/', methods=['GET', 'POST'])
def index():
    page = request.args.get('page', 1, type=int)
    themes = Theme.query
    pagination = themes.paginate(page)
    themes = pagination.items
    return render_template('main/index.html', themes=themes, pagination=pagination)


@main.route('/search', methods=['POST'])
def search():
    key = request.form.get('search')
    if key is not None:
        themes = Theme.query.filter(Theme.title.like('%{}%'.format(key)))
        return render_template('main/index.html', themes=themes)


@main.route('/detail')
def detail():
    title = request.args.get('title')
    order = request.args.get('order')

    theme = Theme.query.filter_by(title=title).first()
    image = Image.query.filter_by(theme=theme, order=order).first()
    return render_template('main/detail.html', image=image, title=title)


@main.route('/ajax', methods=['POST'])
def ajax():
    order = request.form.get('order')
    title = request.form.get('title')
    theme = Theme.query.filter_by(title=title).first()
    image = Image.query.filter_by(theme=theme, order=order).first()
    # 数据库没有该图片 将报错
    if image is not None:
        return jsonify(order=image.order, path=url_for('static', filename=image.path), data='yes')
    return jsonify(data='no')
