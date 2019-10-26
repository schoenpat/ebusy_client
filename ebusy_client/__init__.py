""" Client for eBusy systems """
from requests_html import HTMLSession

from .xpath import BACKEND_LOGIN_CSFR


class EbusyClient:
    url: str
    username: str
    password: str
    session: HTMLSession
    csrf_token: str

    def __init__(self, url, username, password):
        self.url = url if url.endswith('/') else f'{url}/'
        self.username = username
        self.password = password
        self._connect()

    def _connect(self):
        self.session = HTMLSession()
        login_url = f'{self.url}backend/login'
        # We first get the login page to determine the csfr token
        backend_login_page = self.session.get(login_url)
        self.csrf_token = backend_login_page.html.xpath(BACKEND_LOGIN_CSFR)[0].attrs['value']
        login_params = {
            'username': self.username,
            'password': self.password,
            '_csrf': self.csrf_token,
        }
        self.session.post(login_url, params=login_params)
