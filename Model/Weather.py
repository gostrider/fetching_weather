import calendar
from datetime import datetime

from couchbase.exceptions import CouchbaseError

from Utils.Logger import debug, error, get_iso_time


def store(conn, data):
    try:
        conn.insert_multi(data)
    except CouchbaseError as exc:
        for k, res in exc.all_results.items():
            if res.success:
                debug(timestamp=get_iso_time(), message="Insert successful")
            else:
                error(timestamp=get_iso_time(),
                      message="Key {0} failed with error code {1}".format(k, res.rc))


def get_multiple(conn, keys):
    res = conn.get_multi(keys, quiet=True)
    return {k: res.get(k).value for k in res}


def to_key_format(timestamp, country):
    return str(timestamp) + '::' + country


def datetime_to_timestamp(date):
    return calendar.timegm(datetime.strptime(date, '%Y-%m-%dT%H:%M:%S').timetuple())


def get_time_range(start_date, end_date):
    return range(start_date, end_date + 1)


def get_weather_by_timestamp(conn, start_date, end_date, country):
    start_timestamp = datetime_to_timestamp(start_date)
    end_timestamp = datetime_to_timestamp(end_date)
    timestamp_keys = map(lambda t: to_key_format(t, country), get_time_range(start_timestamp, end_timestamp))
    return get_multiple(conn, list(timestamp_keys))
