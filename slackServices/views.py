from django.shortcuts import render

# Create your views here.


def home(request):
    slack_message('slackServices/template/message.slack', {
        'foo': 'test',
    })
    pass

