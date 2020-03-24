from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String())
    date_of_publication = db.Column(db.DateTime())
    headline = db.Column(db.String())
    main_text = db.Column(db.String())
    reports = db.relationship('Report', backref='article')


class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    article_id = db.Column(db.Integer, db.ForeignKey('article.id'))
    syndrome = db.Column(db.String())
    event_date = db.Column(db.String())
    disease = db.Column(db.String())
    locations = db.relationship('Location', backref='report')


class Location(db.Model):
    report_id = db.Column(db.Integer, db.ForeignKey(
        'report.id'), primary_key=True)
    country = db.Column(db.String(), primary_key=True)
    location = db.Column(db.String(), primary_key=True)


def get(limit=1000):
    return db.session.query(Article).order_by(Article.date_of_publication)

