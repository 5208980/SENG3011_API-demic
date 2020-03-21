from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


class Article(db.Model):
    url = db.Column(db.String(), primary_key=True)
    date_of_publication = db.Column(db.String())
    headline = db.Column(db.String())
    main_text = db.Column(db.String())
    reports = db.relationship('Report', backref='article')


class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    article_url = db.Column(db.String(), db.ForeignKey('article.url'))
    syndrome = db.Column(db.String())
    event_date = db.Column(db.String())
    disease = db.Column(db.String())
    locations = db.relationship('Location', backref='report')


class Location(db.Model):
    report_id = db.Column(db.Integer, db.ForeignKey('report.id'), primary_key=True)
    country = db.Column(db.String(), primary_key=True)
    location = db.Column(db.String(), primary_key=True)
