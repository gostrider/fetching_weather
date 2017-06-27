from time import time

from tornado.httpclient import AsyncHTTPClient

from Model import Weather
from Utils import Config
from Utils.Logger import debug, error, get_iso_time


def weather_data(timestamp, response):
    return {
        'country': parse_country_name(response),
        'request_timestamp': timestamp,
        'report_timestamp': parse_timestamp(response),
        **parse_country_weather(response)
    }


def parse_result_lists_json(response):
    return response.get('list', 'error_parsing_list')


def parse_timestamp(results):
    return results.get('dt', 'error_parsing_dt')


def parse_country_name(results):
    return results.get('sys').get('country', 'error_parsing_sys')


def parse_country_weather(results):
    main_part = results.get('main')
    return {
        'temp': main_part.get('temp', 'error_parsing_temp'),
        'humidity': main_part.get('humidity', 'error_parsing_humidity')
    }


def to_couchbase_document(data):
    return join_key(data), data


def join_key(dictionary):
    return str(dictionary.get('request_timestamp', int(time()))) + '::' + dictionary.get('country', 'not_found')


def handle_response(conn, timestamp, response):
    if response.error:
        error(timestamp=get_iso_time(), message=response.error)
    else:
        country_results = parse_result_lists_json(eval(response.body))
        weather_obj = dict(map(lambda r: to_couchbase_document(weather_data(timestamp, r)), country_results))
        debug(timestamp=get_iso_time(), message=weather_obj)
        Weather.store(conn, weather_obj)


def api_key():
    return Config.api_key


def country_codes():
    # HK: 7533612, SG: 1880251
    return map(str, [7533612, 1880251])


def fetch_weather(db_connection=None):
    if db_connection is None:
        error(timestamp=get_iso_time(), message="Couchbase connection error")
    else:
        request_timestamp = int(time())
        url = "http://api.openweathermap.org/data/2.5/group" \
              "?id={AREA}" \
              "&units=metric" \
              "&appid={API_KEY}".format(AREA=",".join(country_codes()),
                                        API_KEY=api_key())
        http_cli = AsyncHTTPClient()
        http_cli.fetch(url, lambda resp: handle_response(db_connection, request_timestamp, resp))
