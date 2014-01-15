from django.conf import settings
from django.utils.encoding import smart_str
from django.template.loader import get_template_from_string
from django.template.context import Context
import requests

SKEBBY_URL = "https://gateway.skebby.it/api/send/smseasy/advanced/http.php"

SKEBBY_METHODS = {
    'basic': 'send_sms_basic',
    'classic': 'send_sms_classic',
    'report': 'send_sms_classic_report',
}

SKEBBY_CHARSETS = ('ISO-8859-1', 'UTF-8')

DEFAULT_MAX_RECIPIENTS = 50000
# this must be agreed with skebby
MAX_RECIPIENTS = 100000

class SkebbySmsError(Exception):
    pass

class SkebbySendError(Exception):
    pass

def _parse_response(response):
    try:
        response.raise_for_status()
        text = response.text.split('&')
        result = {}
        for pair in text:
            k, v = pair.split('=')
            result[k] = v

        if result['status'] == 'failed':
            error_message = result['message']
            error = True
        else:
            error = False
            error_message = ""
    except requests.exceptions.HTTPError as e:
        result = {}
        error_message = e
        error = True
    return { 'response': response, 'error': error, 'message': error_message, 'body': result}

class Sms:
    def __init__(self, text, recipients=None, sender_number=None, sender_string=None, charset=None, ctx=None, headers=None):
        self.template = get_template_from_string(text)
        self.ctx = {} if ctx is None else ctx
        self.text = smart_str(self.template.render(Context(self.ctx)))

        if sender_number is not None and sender_string is not None:
            raise SkebbySmsError("Only one between sender_number and sender_string may be specified")

        self.sender_number = sender_number
        self.sender_string = sender_string

        self.charset = "UTF-8" if charset is None else charset
        if self.charset not in SKEBBY_CHARSETS:
            raise SkebbySmsError("Invalid charset")

        self.headers = {'user-agent': 'Generic Client'} if headers is None else headers
        self.recipients = [] if recipients is None else recipients

        try:
            self.max_recipients = settings.SKEBBY_MAX_RECIPIENTS
        except AttributeError:
            self.max_recipients = DEFAULT_MAX_RECIPIENTS

        if self.max_recipients > MAX_RECIPIENTS:
            self.max_recipients = MAX_RECIPIENTS

    def _check_method(self, method):
        if not method:
            method = 'basic'
        elif method not in SKEBBY_METHODS:
            raise SkebbySendError("Invalid method")
        return SKEBBY_METHODS.get(method)


    def send(self, method=None):
        username = settings.SKEBBY_USERNAME
        password = settings.SKEBBY_PASSWORD

        method = self._check_method(method)

        num_remainders = len(self.recipients)
        if not num_remainders:
            raise SkebbySendError("No recipients")

        ret = []
        while num_remainders:
            remainders = self.recipients[:self.max_recipients]
            payload = {
                'recipients': remainders,
                'method': method,
                'username': username,
                'password': password,
                'text': self.text,
                'sender_number': self.sender_number,
                'sender_string': self.sender_string,
                'charset': self.charset,
            }
            r = requests.post(SKEBBY_URL, data=payload, headers=self.headers)
            num_remainders -= len(remainders)
            ret.append(_parse_response(r))
        return ret

    def send_single(self, ctx, recipient, method=None):
        username = settings.SKEBBY_USERNAME
        password = settings.SKEBBY_PASSWORD

        method = self._check_method(method)
        template = get_template_from_string(self.text)
        text = smart_str(template.render(Context(ctx)))

        payload = {
            'recipients': recipient,
            'method': method,
            'username': username,
            'password': password,
            'text': self.text,
            'sender_number': self.sender_number,
            'sender_string': self.sender_string,
            'charset': self.charset,
        }
        r = requests.post(SKEBBY_URL, data=payload, headers=self.headers)
        return _parse_response(r)

def credit_left():

    username = settings.SKEBBY_USERNAME
    password = settings.SKEBBY_PASSWORD

    payload = {
        'method': 'get_credit',
        'username': username,
        'password': password,
    }

    r = requests.post(SKEBBY_URL, data=payload)
    return _parse_response(r)
