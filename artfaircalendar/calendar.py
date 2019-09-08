import json
import os.path
import time
import urllib.request
import hashlib

import ics

from artfaircalendar.event import Event

N_SECONDS_PER_DAY = 60 * 60 * 24
BASE_URL = "http://www.artfairsservice.com/wp-json/wp/v2/events?filter%%5Bshow%%5D=all&per_page=%d&page=%d"


class Calendar(object):

    def __init__(self):
        self.events = []
        self.position = -1

    @staticmethod
    def from_end_date(end_date) -> "Calendar":
        calendar = Calendar()
        page_number = 1
        found_later_event = False
        while not found_later_event:
            new_events = get_events(page_number)
            for event in new_events:
                if not event.is_valid():
                    continue
                if event.get_end_date() > end_date:
                    found_later_event = True
                else:
                    calendar.events.append(event)
        return calendar

    def __len__(self):
        return len(self.events)

    def __iter__(self):
        self.position = -1
        return self

    def __next__(self):
        self.position += 1
        if self.position < len(self.events):
            return self.events[self.position]
        else:
            raise StopIteration

    def filter_by_city(self, city_name):
        calendar = Calendar()
        calendar.events = [x for x in self.events if x.get_city().lower() == city_name.lower()]
        return calendar

    def filter_by_country(self, country_name):
        calendar = Calendar()
        calendar.events = [x for x in self.events if x.get_country().lower() == country_name.lower()]
        return calendar

    def write_ics(self, filename):
        ics_calendar = ics.Calendar()
        for event in self.events:
            ics_calendar.events.add(event.to_ics_event())
        with open(filename, "w") as f:
            f.writelines(ics_calendar)


def get_events(page_number=1, per_page=100):
    raw_json = get_raw_json(page_number, per_page)
    return [Event(x) for x in raw_json]


def get_raw_json(page_number=1, per_page=100):
    filled_url = BASE_URL % (per_page, page_number)
    filename = hashlib.sha512(filled_url.encode("utf-8")).hexdigest()
    if os.path.exists(filename):
        creation_time = os.stat(filename).st_ctime
        file_is_too_old = time.time() - creation_time > N_SECONDS_PER_DAY
        if not file_is_too_old:
            with open(filename) as f:
                return json.load(f)
        else:
            os.remove(filename)
    with urllib.request.urlopen(filled_url) as url:
        raw_json = json.loads(url.read().decode())
        with open(filename, 'w') as f:
            json.dump(raw_json, f)
        return raw_json