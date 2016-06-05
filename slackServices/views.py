from django.http import HttpResponse
from slackclient import SlackClient
import time
# Create your views here.

def home(request):
    token = "xoxb-48237164960-6wYeaps1Dub5AXptbn6JaTef"
    sc = SlackClient(token)
    if sc.rtm_connect():
        while True:
            print sc.rtm_read()
            time.sleep(1)
    else:
        print "Connection Failed, invalid token?"

    return HttpResponse("")
