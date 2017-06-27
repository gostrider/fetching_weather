from _functools import partial

from couchbase.bucket import Bucket
from tornado import web, ioloop

from Handler.APIHandler import APIHandler
from Request.Weather import fetch_weather
from Utils import Config


def router(couchbase_conn):
    return [
        (r'/weather', APIHandler, {'conn': couchbase_conn}),
    ]


def main():
    cb_conn = Bucket(Config.couchbase_host + '/' + Config.couchbase_bucket)
    fetch_weather_with_conn = partial(fetch_weather, db_connection=cb_conn)
    app = web.Application(router(cb_conn), autoreload=False)
    app.listen(8001)
    main_loop = ioloop.IOLoop.instance()
    # Fetch rate every minute
    timed_fetch = ioloop.PeriodicCallback(fetch_weather_with_conn, 60000, io_loop=main_loop)
    timed_fetch.start()
    main_loop.start()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
