from datetime import datetime, date, time, timezone
import pytz

def check_time_in(location):
    time = pytz.timezone(f'{location}')
    return time




