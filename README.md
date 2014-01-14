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

    sms = Sms("Good {{ festivity }}{% if friend %} {{ friend }}{% endif %}!", ["123456789", "12346788"], sender_string="Your friend", ctx={'festivity': 'birthday'})
    ret = sms.send()
    # api request are splitted by Skebby recipients limits, 50000 default, 100000 if requested
    # returns a list of tuples, each tuple consists of a request and the payload
    failed_requests = [r for r in ret if r[0].status_code != sms.codes.ok]
    if failed_requests:
        print "some errors!"

    # to a special friend
    r = sms.send_single({'festivity': birthday, 'friend': 'Doge' })
    if r[0].status_code != sms.codes.ok:
        print "failed to greet Doge :("

    # check credit
    try:
        credit = credit_left()
    except:
        credit = -1

    if credit < 0:
        print "failed to get credit :("
