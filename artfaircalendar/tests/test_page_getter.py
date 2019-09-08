import datetime
import unittest
from dateutil.relativedelta import *

from artfaircalendar.calendar import Calendar, get_raw_json


class TestPageGetter(unittest.TestCase):

    def setUp(self) -> None:
        self.events = Calendar.from_end_date(datetime.datetime.now() + relativedelta(months=+1)).events

    def test_get_something(self):
        self.assertIsNotNone(self.events)

    def test_at_least_one_element(self):
        self.assertTrue(len(self.events) > 0)

    def test_get_different_pages(self):
        raw_json_1 = get_raw_json(page_number=1)
        raw_json_2 = get_raw_json(page_number=2)
        self.assertNotEqual(raw_json_1, raw_json_2)

    def test_get_different_names(self):
        names = [x.get_name() for x in self.events]
        self.assertTrue("fair" in x.lower() for x in names)

    def test_country(self):
        countries = [x.get_country() for x in self.events]
        self.assertTrue(any(["United States" == x for x in countries]))

    def test_city(self):
        cities = [x.get_city() for x in self.events]
        self.assertTrue(any(["NEW YORK" == x for x in cities]) or any(["PARIS" == x for x in cities]))

    def test_id(self):
        ids = [x.get_id() for x in self.events]
        self.assertTrue(all([type(x) == int for x in ids]))

    def test_link(self):
        links = [x.get_link() for x in self.events]
        self.assertTrue(all(["http" in x for x in links]))

    def test_start_date(self):
        start_dates = [x.get_start_date() for x in self.events]
        self.assertTrue(all([isinstance(x, datetime.datetime) for x in start_dates]))

    def test_end_date(self):
        end_dates = [x.get_end_date() for x in self.events]
        self.assertTrue(all([isinstance(x, datetime.datetime) for x in end_dates]))

    def test_end_after_start(self):
        start_dates = [x.get_start_date() for x in self.events]
        end_dates = [x.get_end_date() for x in self.events]
        self.assertTrue(all([x <= y for x, y in zip(start_dates, end_dates)]))


if __name__ == '__main__':
    unittest.main()
