class Article:
    def __init__(self, url, date_of_publication, headline, main_text, reports, key_terms):
        self._url = url
        self._date_of_publication = date_of_publication
        self._headline = headline
        self._main_text = main_text
        self._reports = reports
        self._key_terms = key_terms

    def get_url(self):
        return self._url

    def set_url(self, url):
        self._url = url

    def get_date_of_publication(self):
        return self._date_of_publication

    def set_date_of_publication(self, date_of_publication):
        self._date_of_publication = date_of_publication

    def get_headline(self):
        return self._headline

    def set_headline(self, headline):
        self._headline = headline

    def get_main_text(self):
        return self._main_text

    def set_main_text(self, url):
        self._main_text = main_text

    def get_reports(self):
        return self._reports

    def set_reports(self, reports):
        self._reports = reports

    def get_key_terms(self):
        return self._key_terms

    def set_terms(self, key_terms):
        self._key_terms.append(key_terms)
