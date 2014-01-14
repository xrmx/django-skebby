from django.test import TestCase
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
