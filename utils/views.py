from django.shortcuts import render
import time  
import json
from random import randint
from django.http import HttpResponse

# Create your views here.
def get_countdown(request):
  seconds       = 3600 * randint(24,50)
  hour,second   = divmod(seconds,60*60)
  minute,second = divmod(second,60)
  day,hour      = divmod(hour,24)

  time = {
    'day'       : day,
    'hour'      : hour,
    'minute'    : minute,
    'second'    : second,
  }
  return HttpResponse(json.dumps({'seconds':seconds}))