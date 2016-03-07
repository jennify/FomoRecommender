# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-07 08:45
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import jsonfield.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Attraction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('placeID', models.CharField(max_length=50)),
                ('rawData', jsonfield.fields.JSONField()),
                ('groupID', models.CharField(max_length=50)),
                ('aggregatedVote', models.FloatField()),
                ('numVotes', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='FullItinerary',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('groupID', models.CharField(max_length=50)),
                ('tripName', models.CharField(max_length=50)),
                ('location', models.CharField(max_length=50)),
                ('radius', models.CharField(max_length=50)),
                ('numDays', models.IntegerField()),
                ('currentItinerary', jsonfield.fields.JSONField()),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.FloatField()),
                ('attraction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fomoapp.Attraction')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='fomoapp.User')),
            ],
        ),
        migrations.AddField(
            model_name='fullitinerary',
            name='travellers',
            field=models.ManyToManyField(to='fomoapp.User'),
        ),
        migrations.AddField(
            model_name='attraction',
            name='sentToClient',
            field=models.ManyToManyField(to='fomoapp.User'),
        ),
    ]