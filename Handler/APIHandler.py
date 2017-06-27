import tornado.web

from Model import Weather


class APIHandler(tornado.web.RequestHandler):
    def __init__(self, application, request, **kwargs):
        super().__init__(application, request, **kwargs)
        self.conn = kwargs['conn']

    def initialize(self, conn):
        pass

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    def check_origin(self, origin):
        return True

    def data_received(self, chunk):
        pass

    def get(self, *args, **kwargs):
        res = Weather.get_weather_by_timestamp(self.conn,
                                               self.get_argument('start'),
                                               self.get_argument('end'),
                                               self.get_argument('city'))
        self.write(drop_none(res))


def drop_none(result):
    return {k: result.get(k) for k in result if result.get(k) is not None}
