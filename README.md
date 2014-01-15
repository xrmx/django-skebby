django-skebby
===================

A simple Django app to send sms with Skebby.

Usage
-----

In settings.py:

    SKEBBY_USERNAME = 'yourskebbyusername'
    SKEBBY_PASSWORD = 'yourskebbypassword'

In your code:

    from django_skebby.utils import Sms, credit_left

    sms = Sms("Good {{ festivity }}{% if friend %} {{ friend }}{% endif %}!", ["39123456789", "3912346788"], sender_string="Your friend", ctx={'festivity': 'birthday'})
    ret = sms.send()
    # api request are splitted by Skebby recipients limits, 50000 default, 100000 if requested
    # returns a list of tuples, each tuple consists of a request and the payload
    failed_requests = [r for r in ret['body'] if r['error']]
    if failed_requests:
        print "some errors!"

    # to a special friend
    r = sms.send_single({'festivity': birthday, 'friend': 'Doge' }, "3912345679")
    if r['error']:
        print "failed to greet :( %s" % (r['error_message'])

    # check credit
    credit = credit_left()
    if credit['error']:
        print "failed to get credit"
    else:
        print credit['body']
