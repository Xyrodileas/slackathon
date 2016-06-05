import time
import requests
from slackclient import SlackClient

token1 = "xoxp-33332867413-47664138370-48238806789-a52c07b13d"
token2 = "xoxp-48241050165-48254821877-48250938304-86292f0518"
class Slack:
    def __init__(self, client):
        self.ClientConnection = client
        self.DicTags = {}
        self.WaitingQuestion = {}
        self.Channels = []


    def connect(self):
        return self.ClientConnection.rtm_connect()
    def fetch(self):
        return self.ClientConnection.rtm_read()

    def sendMessage(self, chan, txt, usr='ShareWithMe', icon=':robot_face:'):
        self.ClientConnection.api_call("chat.postMessage", channel=chan, text=txt, username=usr, icon_emoji=icon)

class Question:
    def __init__(self, user, question, tags, slack):
        self.userID = user
        self.Question = question
        self.Tags = tags
        self.Slack = slack


def getfirstNameByID(idUser):
    info = sc.api_call("users.info", user=idUser)
    user = info.pop("user")
    profile = user.pop("profile")
    return profile.pop("first_name")



def processIncomingEvent(client, event):
    if commande == "SOF" :
        text = text.replace("SOF", "")
        print text
        print requests.get('https://api.stackexchange.com/2.2/search?order=desc&sort=activity&intitle='+text+'&site=stackoverflow').text
        sendMessage(event.pop("channel"), "Hello "+getfirstNameByID(userID)+", que puis-je faire pour vous ? :tada:")


sc1 = SlackClient(token1)
slack1 = Slack(sc1)
sc2 = SlackClient(token2)
slack2 = Slack(sc2)
listeQuestions = []

if slack1.connect() and slack2.connect():

    listClients = [slack1, slack2]
    while True:
        for client in listClients:
            data = client.fetch()
            for event in data:
                print event
                if event.pop("type") == "message":
                    text = event["text"]
                    channel = event["channel"]
                    commande = text.split(" ")[0]
                    if "user" in event:
                        userID = event["user"]
                    print text
                    print userID
                    # Command to setup the themes for a channel
                    if commande == "SETUP":
                        text = text.replace("SETUP", "")
                        client.sendMessage(channel, "Voici les themes ajoute : " + text)
                        client.Channels.append(channel)
                        client.DicTags[channel] = text.split(" ")
                    # Command to ask a question
                    if commande == "QST" :
                        print "Question pose"
                        text = text.replace("QST", "")
                        client.sendMessage(channel, text)
                        if channel in client.DicTags:
                            client.WaitingQuestion[userID] = Question(userID, text, client.DicTags[channel], client)
                        else:
                            client.sendMessage(channel, "Vous n avez pas definie de themes")
                    # Command to validate a question
                    if commande == "ACK" and userID in client.WaitingQuestion and client.WaitingQuestion[userID]:
                        print "Question valide"
                        listeQuestions.append(client.WaitingQuestion[userID])
        #Traitement des questions
        for question in listeQuestions:
            for client in listClients:
                if question.Slack != client :
                    print client.Channels
                    for channel in client.Channels :
                        client.sendMessage(channel, question.Question)
        listeQuestions = []


        time.sleep(1)
else:
    print "Connection Failed, invalid token?"
