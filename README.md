django-skebby
===================

A simple Django app to send sms with Skebby.

Usage
-----

In settings.py:

    SKEBBY_USERNAME = 'yourskebbyusername'
    SKEBBY_PASSWORD = 'yourskebbypassword'

    # if SSL does not work
    #SKEBBY_URL = "http://gateway.skebby.it/api/send/smseasy/advanced/http.php"

    # If you have *requested and obtained* the raise to 100000 messages per request
    #SKEBBY_MAX_RECIPIENTS = 100000

In your code:

    from django_skebby.utils import Sms, credit_left

    # greetings to some people
    template = "Good {{ festivity }}{% if friend %} {{ friend }}{% endif %}!"
    sms = Sms(template, ["39123456789", "3912346788"], sender_string="Your friend", ctx={'festivity': 'birthday'})
    ret = sms.send()
    # Skebby has a recipient limit of 50000 numbers that can be raised to 100000 on request
    # The app will take care of itself depending on settings.SKEBBY_MAX_RECIPIENTS
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
