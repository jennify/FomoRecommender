from __future__ import unicode_literals

from django.db import models
from jsonfield import JSONField

# class Group(models.Model):
#   groupID = models.CharField(max_length=50)
#   cursor = models.CharField(max_length=50)

class Attraction(models.Model):
    placeID = models.CharField(max_length=50)
    rawData = JSONField()
    groupID = models.CharField(max_length=50)

    @classmethod
    def createAttractionsFromJSON(self, json, groupID="FakeGroupID"):
        attractions = json["results"]
        objs = []
        for attraction in attractions:
            placeID = attraction["place_id"]
            a = Attraction(placeID=placeID, rawData=attraction, groupID=groupID)
            a.save()
            objs.append(a)
        return objs

    @classmethod
    def createAttractionFromJSON(self, json, groupID="FakeGroupID"):
        placeID = json["place_id"]
        a = Attraction(placeID=placeID, rawData=json, groupID=groupID)
        a.save()

# class Preference(models.Model):
#   name = models.CharField(max_length=50)


class User(models.Model):
  email = models.EmailField()
  firstName = models.CharField(max_length=50)
  lastName = models.CharField(max_length=50)
  # avatarImageUrl = models.URLField()
#   preferences = models.ManyToManyField(Preference)

class FullItinerary(models.Model):
  ID = models.CharField(max_length=50)
  travellers = models.ManyToManyField(User)
  tripName = models.CharField(max_length=50)
  # startDate = models.DateField()
  # endDate = models.DateField()
  # city = models.CharField(max_length=50)
#   coverPhotoURL = models.URLField()

# class Attraction(models.Model):
#   attraction_name = models.CharField(max_length=50)
#   types = models.CharField(max_length=50) # String for Attraction Type
#   location = models.CharField(max_length=50)
#   rating = models.FloatField()
#   city = models.CharField(max_length=50)

# class Review(models.Model):
#   attraction= models.ForeignKey(Attraction)
#   text = models.TextField()

# class Images(models.Model):
#   attraction = models.ForeignKey(Attraction)
#   url = models.URLField()

# class VotedEvent(models.Model):
#   # Called trip events
#   fullItinerary = models.ForeignKey(FullItinerary)
#   attraction = models.OneToOneField(Attraction)
#   ID = models.CharField(max_length=50)
#   eventType = models.CharField(max_length=50)
#   aggregatedVote = models.FloatField()
#   vote = models.FloatField()

# class Dislikes(models.Model):
#   votedEvent = models.ForeignKey(VotedEvent)
#   user = models.ManyToManyField(User)

# class Likes(models.Model):
#   votedEvent = models.ForeignKey(VotedEvent)
#   user = models.ManyToManyField(User)

# class Neutrals(models.Model):
#   votedEvent = models.ForeignKey(VotedEvent)
#   user = models.ManyToManyField(User)

# class SentToClient(models.Model):
#   votedEvent = models.ForeignKey(VotedEvent)
#   user = models.ManyToManyField(User)

# class DayItinerary(models.Model):
#   # Represents the itinerary for a day
#   fullItinerary = models.ForeignKey(FullItinerary)
#   tripEvents = models.ManyToManyField(VotedEvent)


