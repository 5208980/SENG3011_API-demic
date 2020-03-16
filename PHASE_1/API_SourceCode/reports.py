class Reports:
    def __init__(self, event_date, locations, disease, syndrome):
        self._event_date = event_date
        self._locations = locations
        self._disease = disease
        self._syndrome = syndrome

    def get_event_date(self):
        return self._event_date

    def set_url(self, event_date):
        self._event_date = event_date

    def get_locations(self):
        return self._locations

    def set_locations(self, locations):
        self._locations = locations

    def get_disease(self):
        return self._disease

    def set_disease(self, disease):
        self._disease = disease

    def get_syndrome(self):
        return self._syndrome

    def set_syndrome(self, syndrome):
        self._syndrome = syndrome
