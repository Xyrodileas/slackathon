import time
import requests
from slackclient import SlackClient
import random

botname = "ThotBot"
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

    def sendMessage(self, chan, txt, attach="", usr=botname, icon=':robot_face:'):
        self.ClientConnection.api_call("chat.postMessage", attachments=attach, channel=chan, text=txt, username=usr, icon_emoji=icon)

class Question:
    def __init__(self, user, question, tags, slack, chan):
        self.userID = user
        self.Question = question
        self.Tags = tags
        self.Slack = slack
        self.ID = random.randint(1, 1000)
        self.Channel = chan

class Message(object):
    @classmethod
    def goodAtachment(cls, msg):
        return '[{"pretext": "", "text": "'+msg+'"}]'

def getfirstNameByID(client, idUser):
    info = client.ClientConnection.api_call("users.info", user=idUser)
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
waitingForAnswer = []
currentTS = time.time()
if slack1.connect() and slack2.connect():

    listClients = [slack1, slack2]
    while True:
        for client in listClients:
            data = client.fetch()
            for event in data:
                print event
                if event.pop("type") == "message":
                    if "text" in event:
                        text = event["text"]
                    if "ts" in event:
                        timestamp = event["ts"]
                        if float(timestamp)-currentTS < 0 :
                            continue
                    channel = event["channel"]
                    commande = text.split(" ")[0]
                    if "user" in event:
                        userID = event["user"]
                    if "username" in event:
                        if event["username"] == botname:
                            continue
                    print text
                    print userID
                    # Command to setup the themes for a channel
                    if commande == "SETUP":
                        text = text.replace("SETUP ", "")
                        client.sendMessage(channel, "*Changement des themes*", Message.goodAtachment("Voici les themes du channel : " + text))
                        client.Channels.append(channel)
                        client.DicTags[channel] = text.split(" ")
                    # Command to ask a question
                    if commande == "QST" :
                        text = text.replace("QST ", "")
                        client.sendMessage(channel, "*Etes vous sur de vouloir poser cette question ?*", Message.goodAtachment(text))
                        if channel in client.DicTags:
                            client.WaitingQuestion[userID] = Question(userID, text, client.DicTags[channel], client, channel)
                        else:
                            client.sendMessage(channel, "Vous n avez pas definie de themes")
                    # Command to validate a question
                    if commande == "ACK" and userID in client.WaitingQuestion and client.WaitingQuestion[userID]:
                        listeQuestions.append(client.WaitingQuestion[userID])
                        client.sendMessage(channel, "*Question envoye !*", Message.goodAtachment(client.WaitingQuestion[userID].Question))
                        del client.WaitingQuestion[userID]
                    if commande == "ASW":
                        text = text.replace("ASW ", "")
                        idQuestion = text.split(" ")[0]
                        print idQuestion
                        text = text.replace(idQuestion, "")
                        for question in waitingForAnswer:
                            if question.ID == int(idQuestion):
                                print question.ID
                                client.sendMessage(channel, "*Reponse envoye !*", Message.goodAtachment(text))
                                name = getfirstNameByID(client, userID)
                                question.Slack.sendMessage(question.Channel, "*Reponse a votre question de "+name+"!*", Message.goodAtachment(text))


        #Traitement des questions
        for question in listeQuestions:
            for client in listClients:
                if question.Slack != client :
                    print client.Channels
                    for channel in client.Channels :
                        for tag in client.DicTags[channel]:
                            if tag in question.Tags:
                                client.sendMessage(channel, "*Nouvelle question !*", Message.goodAtachment("ID : "+ str(question.ID) + " " + question.Question))
            waitingForAnswer.append(question)
        listeQuestions = []


        time.sleep(1)
else:
    print "Connection Failed, invalid token?"
