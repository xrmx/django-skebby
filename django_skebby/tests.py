from django.test import TestCase
from django.conf import settings
from django.test.utils import override_settings
from django_skebby.utils import Sms, credit_left, SkebbySmsError

class TestSkebby(TestCase):
    def test_basic_sms(self):
        sms = Sms("Hi there!", ["123456789"], sender_string="Your Friend")
        self.assertEqual(sms.headers, {'user-agent': 'Generic Client'})

    def test_template_rendering(self):
        sms = Sms("Happy {{ festivity }}!", ["123456789"], sender_string="Your friend", ctx={'festivity': 'birthday'})
        self.assertEqual(sms.text, "Happy birthday!")

    def test_sender_num_string(self):
        ret = False
        try:
            sms = Sms("Hi there!", ["123456789"], sender_string="Your friend", sender_number="123456789")
        except SkebbySmsError:
            ret = True
        self.assertEqual(ret, True)

    def test_charset(self):
        ret = False
        try:
            sms = Sms("Hi there!", ["123456789"], charset="foo",  sender_number="123456789")
        except SkebbySmsError:
            ret = True
        self.assertEqual(ret, True)

    def test_credit_left(self):
        r = credit_left()
        credit = r['body']
        self.assertEqual(True, 'credit_left' in credit)
        self.assertEqual(True, 'classic_sms' in credit)
        self.assertEqual(True, 'basic_sms' in credit)

    def test_send(self):
        try:
           test_number = settings.SKEBBY_TEST_NUMBER
        except AttributeError:
           return

        sms = Sms("Hi there!", [test_number], sender_string="Your Friend")
        ret = sms.send()
        failed_requests = [r for r in ret if r['error']]
        succesful_requests = [r for r in ret if not r['error']]
        self.assertEqual(len(failed_requests) + len(succesful_requests), 1)

    def test_send_single(self):
        try:
           test_number = settings.SKEBBY_TEST_NUMBER
        except AttributeError:
           return

        sms = Sms("Hi {{ friend }}!", sender_string="Your Friend")
        ret = sms.send_single({'friend': 'Doge'}, test_number)
        self.assertEqual(True, 'error' in ret)
