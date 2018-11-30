from . import db


class Image(db.Model):
    __tablename__ = 'images'

    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String)
    order = db.Column(db.String)
    theme_id = db.Column(db.Integer, db.ForeignKey('themes.id'))

    def __repr__(self):
        return '<Image %r>' % self.id


class Theme(db.Model):
    __tablename__ = 'themes'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    images = db.relationship('Image', backref='theme')

    def __repr__(self):
        return '<Theme %r>' % self.id



