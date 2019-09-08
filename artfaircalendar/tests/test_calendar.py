import datetime
import os
import unittest

from dateutil.relativedelta import relativedelta

from artfaircalendar.calendar import Calendar


class TestCalendar(unittest.TestCase):

    def setUp(self) -> None:
        self.calendar = Calendar.from_end_date(datetime.datetime.now() + relativedelta(months=+12))

    def test_filter_by_city(self):
        city_name = "Paris"
        by_city = self.calendar.filter_by_city(city_name)
        self.assertNotEqual(len(by_city), 0)
        self.assertTrue(all([x.get_city().lower() == city_name.lower() for x in by_city]))

    def test_filter_by_country(self):
        country_name = "France"
        by_country = self.calendar.filter_by_country(country_name)
        self.assertNotEqual(len(by_country), 0)
        self.assertTrue(all([x.get_country() == country_name for x in by_country]))

    def test_write_ics(self):
        self.calendar.write_ics("test.ics")
        self.assertTrue(os.path.exists("test.ics"))
        os.remove("test.ics")


if __name__ == '__main__':
    unittest.main()
