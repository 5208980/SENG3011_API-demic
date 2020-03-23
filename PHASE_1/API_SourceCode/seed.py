from app import db, app
from scraper import scrape
import datetime

def main():
    with app.app_context():
        db.create_all()

    start_date = datetime.datetime(2020, 2, 25)
    end_date = datetime.datetime.now()

    articles = scrape(start_date, end_date)
    print(articles)

if __name__ == '__main__':
    main()
