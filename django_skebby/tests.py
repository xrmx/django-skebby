from django.test import TestCase
from django.test.utils import override_settings
from django_skebby.utils import Sms, skebby_credit_left, SkebbySmsError, SkebbySendError

class TestSkebby(TestCase):
    def test_basic_sms(self):
        sms = Sms("Hi there!", ["123456789"], sender_string="Your Friend")
        self.assertEqual(sms.headers, {'user-agent': 'Generic Client'})

    def test_template_rendering(self):
        sms = Sms("Happy {{ festivity }}!", ["123456789"], sender_string="Your friend", ctx={'festivity': 'birthday'})
        self.assertEqual(sms.text, "Happy birthday!")

    def test_invalid_sender_num_string(self):
        ret = False
        try:
            sms = Sms("Hi there!", ["123456789"], sender_string="Your friend", sender_number="123456789")
        except SkebbySmsError:
            ret = True
        self.assertEqual(ret, True)

    def test_invalid_sender_string(self):
        ret = False
        try:
            sms = Sms("Hi there!", ["123456789"], sender_string="Longer than 11 chars")
        except SkebbySmsError:
            ret = True
        self.assertEqual(ret, True)

    def test_invalid_sender_string_basic_method(self):
        ret = False
        sms = Sms("Hi there!", ["123456789"], sender_string="Me")
        try:
            sms.send(method="basic")
        except SkebbySendError:
            ret = True
        self.assertEqual(ret, True)

    def test_invalid_sender_number_basic_method(self):
        ret = False
        sms = Sms("Hi there!", ["123456789"], sender_number="39123456789")
        try:
            sms.send(method="basic")
        except SkebbySendError:
            ret = True
        self.assertEqual(ret, True)

    def test_invalid_charset(self):
        ret = False
        try:
            sms = Sms("Hi there!", ["123456789"], charset="foo",  sender_number="123456789")
        except SkebbySmsError:
            ret = True
        self.assertEqual(ret, True)

    def test_credit_left(self):
        r = skebby_credit_left()
        credit = r.skebby_response
        self.assertEqual(True, 'credit_left' in credit)
        self.assertEqual(True, 'classic_sms' in credit)
        self.assertEqual(True, 'basic_sms' in credit)

    def test_send(self):
        sms = Sms("Hi there!", ["39123456789"], sender_string="Your Friend")
        ret = sms.send(method="test")
        failed_requests = [r for r in ret if r.skebby_error]
        succesful_requests = [r for r in ret if not r.skebby_error]
        self.assertEqual(len(failed_requests) + len(succesful_requests), 1)

    def test_send_single(self):
        sms = Sms("Hi {{ friend }}!", sender_string="Your Friend")
        ret = sms.send_single({'friend': 'Doge'}, "39123456789", method="test")
        self.assertEqual(sms.text, "Hi Doge!")
        self.assertEqual(False, ret.skebby_error)
        self.assertEqual("", ret.skebby_message)

    @override_settings(SKEBBY_DEFAULT_METHOD='foobar')
    def test_default_invalid_method(self):
        ret = False
        sms = Sms("Hi there!", ["123456789"])
        try:
            sms.send()
        except SkebbySendError:
            ret = True
        self.assertEqual(ret, True)
