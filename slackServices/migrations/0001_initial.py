# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-05 04:51
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import jsonfield.fields
import picklefield.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.TextField(null=True)),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Channel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('is_channel', models.BinaryField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('topic', jsonfield.fields.JSONField()),
                ('last_read', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.IntegerField()),
                ('date', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('editable', models.BinaryField(default=False)),
                ('num_stars', models.PositiveIntegerField(default=0)),
                ('channels', models.ManyToManyField(to='slackServices.Channel')),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.TextField()),
                ('is_channel', models.BinaryField()),
                ('is_question', models.BinaryField()),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Reputation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count_vote', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', models.BinaryField(default=True)),
                ('instance', picklefield.fields.PickledObjectField(editable=False)),
                ('channels', models.ManyToManyField(to='slackServices.Channel')),
            ],
        ),
        migrations.CreateModel(
            name='Stat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count_question', models.PositiveIntegerField(default=0)),
                ('count_response', models.PositiveIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(unique=True)),
                ('count_index', models.PositiveIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.TextField()),
                ('last_name', models.TextField()),
                ('active', models.BinaryField(default=True)),
                ('profile', jsonfield.fields.JSONField()),
                ('reputation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='slackServices.Reputation')),
                ('user_stat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='slackServices.Stat')),
            ],
        ),
        migrations.AddField(
            model_name='stat',
            name='interest_tags',
            field=models.ManyToManyField(to='slackServices.Tag'),
        ),
        migrations.AddField(
            model_name='message',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='author', to='slackServices.User'),
        ),
        migrations.AddField(
            model_name='message',
            name='tags',
            field=models.ManyToManyField(to='slackServices.Tag'),
        ),
        migrations.AddField(
            model_name='message',
            name='to_users',
            field=models.ManyToManyField(related_name='receivers', to='slackServices.User'),
        ),
        migrations.AddField(
            model_name='file',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='slackServices.User'),
        ),
        migrations.AddField(
            model_name='file',
            name='tags',
            field=models.ManyToManyField(to='slackServices.Tag'),
        ),
        migrations.AddField(
            model_name='event',
            name='receivers',
            field=models.ManyToManyField(to='slackServices.User'),
        ),
        migrations.AddField(
            model_name='channel',
            name='members',
            field=models.ManyToManyField(to='slackServices.User'),
        ),
        migrations.AddField(
            model_name='bot',
            name='session',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='slackServices.Session'),
        ),
    ]
