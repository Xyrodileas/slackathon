from __future__ import unicode_literals

from django.db import models
from picklefield.fields import PickledObjectField
from jsonfield import JSONField



class Session(models.Model):
    etat = models.BinaryField(default=True)
    instance = PickledObjectField()


class Bot(models.Model):
    token = models.TextField(null=True)
    name = models.CharField(max_length=20)
    session = models.ForeignKey(to=Session)


class Tag(models.Model):
    name = models.TextField(unique=True)
    count_index = models.PositiveIntegerField(default=0)


class Stat(models.Model):
    interest_tags = models.ManyToManyField(to=Tag)
    count_question = models.PositiveIntegerField(default=0)
    count_response = models.PositiveIntegerField(default=0)


class Reputation(models.Model):
    count_vote = models.PositiveIntegerField()


class User(models.Model):
    first_name = models.TextField(null=False)
    last_name = models.TextField(null=False)
    active = models.BinaryField(default=True)
    profile = JSONField()
    reputation = models.ForeignKey(to=Reputation)
    user_stat = models.ForeignKey(to=Stat)


class Message(models.Model):
    type = models.TextField(null=False)
    is_channel = models.BinaryField(null=False)
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(to=User, related_name="author")
    to_users = models.ManyToManyField(to=User, related_name="receivers")
    tags = models.ManyToManyField(to=Tag)


class Channel(models.Model):
    name = models.TextField(null=False)
    is_channel = models.BinaryField(default=True)# pas forcement utile
    created = models.DateTimeField(auto_now_add=True)# pas forcement utile
    members = models.ManyToManyField(to=User)# pas forcement utile
    topic = JSONField()
    last_read = models.DateTimeField()# pas forcement utile


class File(models.Model):
    name = models.TextField(null=False)
    editable = models.BinaryField(default=False)
    channels = models.ManyToManyField(to=Channel)
    num_stars = models.PositiveIntegerField(default=0)
    creator = models.ForeignKey(to=User)
    tags = models.ManyToManyField(to=Tag)


class Event(models.Model):
    type = models.IntegerField()
    date = models.DateTimeField()
    receivers = models.ManyToManyField(to=User)


