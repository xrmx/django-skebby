from django.conf.urls import *

urlpatterns = patterns('django_skebby.views',
    (r'credit_left/$', 'credit_left', {}, 'skebby-credit-left'),
)
