from __future__ import unicode_literals

from django.db import models
from jsonfield import JSONField
import json

class User(models.Model):
    email = models.EmailField()
    name = models.CharField(max_length=50)
    avatarImageUrl = models.URLField(blank=True)

    def encode(self):
        return {
            "email": self.email,
            "name": self.name,
            "profileImageUrl": self.avatarImageUrl
        }

    def __repr__(self):
        return "%s:%s" % (self.name, self.email)

# class Preference(models.Model):
#     user = models.ForeignKey(User)
#     name = models.CharField(max_length=50)
#     rating = models.FloatField()

class Attraction(models.Model):
    placeID = models.CharField(max_length=50)
    rawData = JSONField()
    groupID = models.CharField(max_length=50)
    sentToClient = models.ManyToManyField(User)
    aggregatedVote = models.FloatField()
    numVotes = models.IntegerField()
    rawPlaceDetails = JSONField()
    # types = models.CharField(max_length=50) # String for Attraction Type

    @classmethod
    def createAttractionsFromJSON(self, json, groupID="FakeGroupID"):
        attractions = json["results"]
        objs = []
        for attraction in attractions:
            placeID = attraction["place_id"]
            query = Attraction.objects.filter(placeID=placeID, groupID=groupID)
            if len(query) > 0:
                a = query[0]
            else:
                print "Creating new attraction %s", placeID
                a = Attraction(placeID=placeID, rawData=attraction, groupID=groupID,
                    aggregatedVote=0.0, numVotes=0)
                a.save()
            objs.append(a)
        return objs

    def encode(self):
        likes = []
        dislikes = []
        neutral = []
        photos = []
        itinerary = FullItinerary.objects.get(groupID=self.groupID)

        for v in Vote.objects.filter(attraction=self):
            user = v.user
            if v.rating > 0:
                likes.append(user.encode())
            elif v.rating < 0:
                dislikes.append(user.encode())
            elif v.rating == 0:
                neutral.append(user.encode())

        for p in Photo.objects.filter(attraction=self):
            photos.append(p.url)

        return {
            "placeID": self.placeID,
            "vote": self.aggregatedVote,
            "likes": likes,
            "dislikes": dislikes,
            "neutral": neutral,
            "groupID": self.groupID,
            "rawData": self.rawData,
            "aggregatedVote": self.aggregatedVote,
            "photos": photos,
        }

class Photo(models.Model):
    attraction = models.ForeignKey(Attraction)
    url = models.CharField(max_length=50)

    @classmethod
    def createFromJSON(self, url, attraction):
        p = Photo(
            attraction= attraction,
            url= url,
        )
        p.save()
        return p

class FullItinerary(models.Model):
    groupID = models.CharField(max_length=50)
    travellers = models.ManyToManyField(User)
    tripName = models.CharField(max_length=50)
    location = models.CharField(max_length=50)
    radius = models.CharField(max_length=50)
    numDays = models.IntegerField()
    currentItinerary = JSONField()
    startDate = models.CharField(max_length=50)
    createDate = models.CharField(max_length=50)
    # coverPhotoURL = models.URLField()

    def encode(self):
        response = {"groupID": self.groupID, "tripName": self.tripName}
        json_travellers = []
        for traveller in self.travellers.all():
            json_travellers.append(traveller.encode())
        response["travellers"] = json_travellers

        self.refreshItinerary()
        response["itinerary"] = self.currentItinerary["itinerary"]

        response["numDays"] = self.numDays
        response["startDate"] = self.startDate
        response["createDate"] = self.createDate

        return response

    def refreshItinerary(self):
        itinerary = []
        attractions = Attraction.objects.filter(groupID=self.groupID).order_by("-aggregatedVote")
        for a in attractions:
            itinerary.append(a.encode())
        self.currentItinerary = {
            "itinerary": itinerary
        }
        self.save()
        return itinerary

    def __repr__(self):
        return "%s:%s" % (self.groupID, self.tripName)

# class DayItinerary(models.Model):
#     # Represents the itinerary for a day
#     fullItinerary = models.ForeignKey(FullItinerary)
#     dayNum = models.IntegerField()
#     restaurants = models.ManyToManyField(Attraction)
#     tripEvents = models.ManyToManyField(Attraction)


# class VotedEvent(models.Model):
#   # Called trip events
#   fullItinerary = models.ForeignKey(FullItinerary)
#   attraction = models.OneToOneField(Attraction)
#   ID = models.CharField(max_length=50)
#   eventType = models.CharField(max_length=50)
#   aggregatedVote = models.FloatField()
#   vote = models.FloatField()

class Vote(models.Model):
    attraction = models.ForeignKey(Attraction)
    rating = models.FloatField()
    user = models.OneToOneField(User)

    @classmethod
    def castVote(self, attraction, rating, user):
        v = Vote(
            attraction=attraction,
            rating=vote_points,
            user=user)
        v.save()

        oldNumVotes = attraction.numVotes
        attraction.numVotes = oldNumVotes + 1

        sumOfOldVotes = attraction.aggregatedVote * oldNumVotes
        attraction.aggregatedVote = (sumOfOldVotes + vote_points) / (oldNumVotes + 1)

        attraction.save()

        return v



