django-skebby
===================

A simple Django app to send sms by Skebby.

Usage
-----

In settings.py:

    SKEBBY_USERNAME = 'yourskebbyusername'
    SKEBBY_PASSWORD = 'yourskebbypassword'

    # If SSL cert is not valid
    SKEBBY_VERIFY_SSL_CERTIFICATE = False

    # If SSL does not work at all
    #SKEBBY_URL = "http://gateway.skebby.it/api/send/smseasy/advanced/http.php"

    # If you have *requested and obtained* the raise to 100000 messages per request
    #SKEBBY_MAX_RECIPIENTS = 100000

    # default method is classic
    SKEBBY_DEFAULT_METHOD = "basic"

In your code:

    from django_skebby.utils import Sms, skebby_credit_left

    # greetings to some people
    template = "Good {{ festivity }}{% if friend %} {{ friend }}{% endif %}!"
    ctx = {'festivity': 'birthday'}
    sms = Sms(template, ["39123456789", "3912346788"], sender_string="Your friend", ctx=ctx)
    ret = sms.send()
    # Skebby has a recipient limit of 50000 numbers that can be raised to 100000 on request
    # The app will take care of itself depending on settings.SKEBBY_MAX_RECIPIENTS
    failed_requests = [r for r in ret if r.skebby_error]
    if failed_requests:
        print "some errors!"

    # to a special friend
    ctx = {'festivity': birthday, 'friend': 'Doge'}
    r = sms.send_single(ctx, "3912345679")
    if r.skebby_error:
        print "failed to greet :( %s" % (r.skebby_response)

    # check credit
    credit = skebby_credit_left()
    if credit.skebby_error:
        print "failed to get credit"
    else:
        print credit.skebby_response

A view that returns the credit in json format is available, to enable it add the app:

    INSTALLED_APPS = (
        ...
        'django_skebby',
    )

include the urls:

    url(r'^skebby/', include('django_skebby.urls')),

add use it:

    <script>
    $.get('/skebby/credit_left/', function(data) {
        console.log(data['credit_left']);
        console.log(data['classic_sms']);
        console.log(data['basic_sms']);
    });
    </script>
