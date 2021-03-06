from social.strategies.base import BaseStrategy


TEST_URI = 'http://myapp.com'
TEST_HOST = 'myapp.com'


class Redirect(object):
    def __init__(self, url):
        self.url = url


class TestStrategy(BaseStrategy):

    def __init__(self, *args, **kwargs):
        self._request_data = {}
        self._settings = {}
        self._session = {}
        super(TestStrategy, self).__init__(*args, **kwargs)

    def redirect(self, url):
        return Redirect(url)

    def get_setting(self, name):
        """Return value for given setting name"""
        return self._settings[name]

    def html(self, content):
        """Return HTTP response with given content"""
        return content

    def render_html(self, tpl=None, html=None, context=None):
        """Render given template or raw html with given context"""
        return tpl or html

    def request_data(self, merge=True):
        """Return current request data (POST or GET)"""
        return self._request_data

    def request_host(self):
        """Return current host value"""
        return TEST_HOST

    def session_get(self, name, default=None):
        """Return session value for given key"""
        return self._session.get(name, default)

    def session_set(self, name, value):
        """Set session value for given key"""
        self._session[name] = value

    def session_pop(self, name):
        """Pop session value for given key"""
        return self._session.pop(name, None)

    def build_absolute_uri(self, path=None):
        """Build absolute URI with given (optional) path"""
        return TEST_URI + (path or '')

    def set_settings(self, values):
        self._settings.update(values)

    def set_request_data(self, values):
        self._request_data.update(values)
