class Locations:
    def __init__(self, country, location, code):
        self._country = country
        self._location = location
        self._code = code

    def get_country(self):
        return self._country

    def set_country(self, country):
        self._country = country

    def get_location(self):
        return self._location

    def set_location(self, location):
        self._location = location

    def get_code(self):
        return self._code
