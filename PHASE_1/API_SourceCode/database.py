import os
import psycopg2
from article import Article
from reports import Reports
from locations import Locations

DATABASE_URL = os.environ['DATABASE_URL']

conn = psycopg2.connect(DATABASE_URL, sslmode='require')

cursor = conn.cursor()


def insert(article):
    cursor.execute("INSERT INTO articles (url, date_of_publication, headline, main_text) VALUES (%s, %s, %s, %s)",
                   (article.get_url(), article.get_date_of_publication(), article.get_headline(), article.get_main_text()))
    
    report = article.get_reports()

    cursor.execute("INSERT INTO reports (article_url, syndrome, event_date, disease) VALUES (%s, %s, %s, %s) RETURNING id",
                (article.get_url(), report.get_syndrome(), report.get_event_date(), report.get_disease()))

    report_id = cursor.fetchone()[0]

    for location in report.get_locations():
        cursor.execute("INSERT INTO locations (report_id, country, location) VALUES (%s, %s, %s)",
                (report_id, location.get_country(), location.get_location()))

    conn.commit()