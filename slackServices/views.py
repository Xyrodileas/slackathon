from django.http import HttpResponse
from slacker import Slacker
# Create your views here.


def home(request):

    slack = Slacker('xoxp-33332867413-46170708884-48203831046-a82fe20e4a')

    # Send a message to #general channel
    slack.chat.post_message('#brainfreeze', 'Hello fellow slackers!')

    # Get users list
    response = slack.users.list()
    users = response.body['members']

    # Upload a file
    #slack.files.upload('hello.txt')
    html = "<html><body>It is now.</body></html>"
    return HttpResponse(html)
