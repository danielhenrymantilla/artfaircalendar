# Art Fair Calendar

Transforms the data from the Art Fairs Service Website into an ICS calendar.

## Installation

```bash
git clone https://github.com/Aunsiels/artfaircalendar
cd artfaircalendar
pip3 install -r requirements.txt
export PYTHONPATH=$PYTHONPATH:`pwd`
```

## Simple use case

```python3
import datetime
from dateutil.relativedelta import relativedelta
from artfaircalendar.calendar import Calendar
calendar = Calendar.from_end_date(datetime.datetime.now() + relativedelta(months=+1))
calendar = calendar.filter_by_country("France")
calendar.write_ics("my_calendar.ics")
```
