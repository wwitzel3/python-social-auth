from social.utils import parse_qs
from social.backends.oauth import BaseOAuth1, BaseOAuth2, OAuthAuth


RDIO_API = 'https://www.rdio.com/api/1/'


class BaseRdio(OAuthAuth):
    ID_KEY = 'key'

    def get_user_details(self, response):
        return {
            'username': response['username'],
            'first_name': response['firstName'],
            'last_name': response['lastName'],
            'fullname': response['displayName'],
        }


class RdioOAuth1(BaseRdio, BaseOAuth1):
    """Rdio OAuth authentication backend"""
    name = 'rdio-oauth1'
    REQUEST_TOKEN_URL = 'http://api.rdio.com/oauth/request_token'
    AUTHORIZATION_URL = 'https://www.rdio.com/oauth/authorize'
    ACCESS_TOKEN_URL = 'http://api.rdio.com/oauth/access_token'
    EXTRA_DATA = [
        ('key', 'rdio_id'),
        ('icon', 'rdio_icon_url'),
        ('url', 'rdio_profile_url'),
        ('username', 'rdio_username'),
        ('streamRegion', 'rdio_stream_region'),
    ]

    @classmethod
    def tokens(cls, instance):
        token = super(RdioOAuth1, cls).tokens(instance)
        if token and 'access_token' in token:
            token = parse_qs(token['access_token'])
        return token

    def user_data(self, access_token, *args, **kwargs):
        """Return user data provided"""
        params = {'method': 'currentUser',
                  'extras': 'username,displayName,streamRegion'}
        request = self.oauth_request(access_token, RDIO_API,
                                     params, method='POST')
        try:
            return self.get_json(request.url,
                                 method='POST',
                                 data=request.to_postdata())['result']
        except ValueError:
            return None


class RdioOAuth2(BaseRdio, BaseOAuth2):
    name = 'rdio-oauth2'
    AUTHORIZATION_URL = 'https://www.rdio.com/oauth2/authorize'
    ACCESS_TOKEN_URL = 'https://www.rdio.com/oauth2/token'
    ACCESS_TOKEN_METHOD = 'POST'
    EXTRA_DATA = [
        ('key', 'rdio_id'),
        ('icon', 'rdio_icon_url'),
        ('url', 'rdio_profile_url'),
        ('username', 'rdio_username'),
        ('streamRegion', 'rdio_stream_region'),
        ('refresh_token', 'refresh_token', True),
        ('token_type', 'token_type', True),
    ]

    def user_data(self, access_token, *args, **kwargs):
        try:
            return self.get_json(RDIO_API, data={
                'method': 'currentUser',
                'extras': 'username,displayName,streamRegion',
                'access_token': access_token
            })['result']
        except ValueError:
            return None
