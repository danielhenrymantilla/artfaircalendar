import datetime

import ics


class Event(object):

    def __init__(self, raw_json):
        self.raw_json = raw_json

    def get_name(self):
        return self.raw_json["title"]["rendered"]

    def get_country(self):
        return self.raw_json["country"]

    def get_city(self):
        return self.raw_json["city"]

    def get_id(self):
        return self.raw_json["id"]

    def get_link(self):
        return self.raw_json["url"]

    def get_start_date(self):
        start_raw = self.raw_json["date_formatted"].split(" - ")[0]
        return datetime.datetime.strptime(start_raw, "%d %b, %Y")  # e.g.  28 JUN, 2019

    def get_end_date(self):
        start_raw = self.raw_json["date_formatted"].split(" - ")[1]
        return parse_raw_date(start_raw)

    def is_valid(self):
        return self.get_start_date() <= self.get_end_date()

    def to_ics_event(self):
        return ics.Event(name=self.get_name(),
                         begin=self.get_start_date(),
                         end=self.get_end_date(),
                         uid=str(self.get_id()),
                         url=self.get_link(),
                         location=self.get_city() + ", " + self.get_country())


def parse_raw_date(start_raw):
    extracted_date = datetime.datetime.strptime(start_raw, "%d %b, %Y")  # e.g.  28 JUN, 2019
    return extracted_date