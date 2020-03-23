from app import db, app
from database import Article, Report, Location
from scraper import scrape
import datetime

def main():
    with app.app_context():
        db.create_all()

    start_date = datetime.datetime(2020, 3, 22)
    end_date = datetime.datetime.now()

    articles = scrape(start_date, end_date)

    with app.app_context():
        for article in articles:
            create_article(article)

        db.session.commit()

    print(articles)


def create_article(article):
    reports = []
    locations = []

    report = article.get_reports()

    for location in report.get_locations():
        locations.append(Location(
            country=location.get_country(),
            location=location.get_location()
        ))

    reports.append(Report(
        syndrome=report.get_syndrome(),
        event_date=report.get_event_date(),
        disease=report.get_disease(),
        locations=locations
    ))

    db.session.add(Article(
        url=article.get_url(),
        date_of_publication=article.get_date_of_publication(),
        headline=article.get_headline(),
        main_text=article.get_main_text(),
        reports=reports))


if __name__ == '__main__':
    main()
