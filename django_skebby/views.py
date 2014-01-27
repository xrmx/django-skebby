from django.http import HttpResponse
from django_skebby.utils import skebby_credit_left
import requests
import json

def credit_left(request):
    credit = skebby_credit_left()
    credit_dict = credit.skebby_response if not credit.skebby_error else {}
    return HttpResponse(json.dumps(credit_dict), mimetype="application/json")
