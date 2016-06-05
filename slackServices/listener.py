from models import Session, Tag, Message, User, Channel
from slackclient import SlackClient
import time


def activate_listener(request):
    token1 = "xoxp-33332867413-47664138370-48238806789-a52c07b13d"
    token2 = "xoxp-48241050165-48254821877-48250938304-86292f0518"

    sc1 = SlackClient(token1)
    slack1 = Session(sc1)
    sc2 = SlackClient(token2)
    slack2 = Session(sc2)
    questions_list = Message.objects.filter(is_question=True).get()

    if slack1.connect() and slack2.connect():
        list_sessions = [slack1, slack2]

        while True:
            for session in list_sessions:
                data = session.fetch()

                for event in data:
                    if event.pop("type") == "message":
                        traiter_message(event, session, questions_list)

            traiter_question(list_sessions, questions_list)

            time.sleep(1)
    else:
        print "Connection Failed, invalid token?"


def traiter_message(event, session, questions_list):
    text = event["text"]
    chan = event["channel"]
    command = text.split(" ")[0]
    text = text.replace(command, "")

    if "user" in event:
        user, created = User.objects.get_or_create(id=event["user"])
        message, created = Message.objects.get_or_create(type=command, created_by=user)
        channel, created = Channel.objects.get_or_create(name=chan)

        # Command to setup the themes for a channel
        if command == "SETUP":
            session.sendMessage(channel, "Voici les themes ajoutees : " + text)
            session.channels.add(channel)
            message.tags = get_tags(text)

        if command == "RM":
            session.sendMessage(channel, "Voici les themes supprimees : " + text)
            session.channels.remove(channel)
            message.tags = get_tags(text)

        # Command to ask a question
        if command == "QST":
            session.sendMessage(channel, text)
            if channel in session.DicTags:
                session.WaitingQuestion[user.id] = 1#Question(user_id, text, client.DicTags[channel], client)
            else:
                session.sendMessage(channel, "Vous n\'avez pas defini de themes")
        # Command to validate a question
        if command == "ACK" and user.id in session.WaitingQuestion and session.WaitingQuestion[user.id]:
            print "Question valide"
            questions_list.append(session.WaitingQuestion[user.id])

        user.save()
        message.save()
        channel.save()


def traiter_question(list_sessions, questions_list):
    for question in questions_list:
        for session in list_sessions:
            if question.Slack != session:
                print session.Channels
                for channel in session.Channels:
                    session.sendMessage(channel, question.Question)
                    questions_list.objects.filter(question).delete()


def get_tags(tags):
    tag_array = []
    for tag in tags.split(" "):
        tag, created = Tag.objects.get_or_create(name=tag)
        if created:
            tag.count_index += 1

        tag.save()
        tag_array.append(tag)
    return tag_array


