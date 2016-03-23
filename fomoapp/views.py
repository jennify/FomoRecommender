from django.shortcuts import render

# Create your views here.
from django.http import (
    HttpResponse,
    JsonResponse,
)

import urllib
import requests
import os
from .models import Attraction, FullItinerary, User, Photo
from django.core.exceptions import SuspiciousOperation
from django.views.decorators.csrf import csrf_exempt

def index(request):
    return HttpResponse("Welcome to Fomo's home page! Feelings some fomo? Check out: https://github.com/jennify/Fomo")

def testGooglePlaces(request):
    assert request.method == "GET"
    search_text = request.GET["search_text"]
    # location = request.GET["location"] # "num,num"
    # radius = request.GET["radius"] # in meters

    json = GooglePlacesAPIClient.textSearch(search_text=search_text)
    return JsonResponse(json)

def get_recommendations(request):
    if request.method != "GET":
        raise SuspiciousOperation("GET Request only.")

    groupID = request.GET['groupID']
    email = request.GET['userEmail']
    name = request.GET['name']
    profileImageUrl = request.GET['profileImageUrl']

    user = User.objects.filter(email=email)
    if len(user) == 0 :
        user = get_or_create_user(groupID, email, name, profileImageUrl)
    else:
        user = user[0]
    response = {}
    a_list = []
    attractions = Attraction.objects.filter(groupID=groupID)
    if len(attractions) == 0:
        raise SuspiciousOperation("No attractions or Invalid group ID")

    for a in attractions:
        if True:
        # if user not in a.sentToClient.all():
            a_list.append(a.encode())
            a.sentToClient.add(user)
    response["attractions"] = a_list

    if len(a_list) < 10:
        # TODO(jlee): code to load more attractions with paging

        pass

    return JsonResponse(response)

def get_itineraries_for_user(request):
    if request.method != "GET":
        raise SuspiciousOperation("GET Request only.")

    userEmail = request.GET['userEmail']
    itineraries = FullItinerary.objects.filter(travellers__email=userEmail)
    i_list = []
    for i in itineraries:
        i_list.append(i.encode())
    return JsonResponse({"itineraries": i_list})



@csrf_exempt
def update_itinerary_with_vote(request):
    if request.method != "POST":
        raise SuspiciousOperation("POST Request only.")

    groupID = request.POST['groupID']
    placeID = request.POST['placeID']
    userEmail = request.POST['userEmail']
    user = User.objects.get(email=userEmail)
    attraction = Attraction.objects.get(placeID=placeID, groupID=groupID)[0]

    vote_points = 0
    if 'like' in request.POST:
        vote_points = 1.0
    elif 'dislike' in request.POST:
        vote_points = -1.0
    elif 'neutral' in request.POST:
        vote_points = 0.0
    else:
        raise SuspiciousOperation("Invalid Vote")

    vote = Vote.castVote(
        attraction=attraction,
        rating=vote_points,
        user=user)

    json = FullItinerary.objects.filter(groupID=groupID)[0].encode()
    json["itinerary"]
    return JsonResponse(json)

@csrf_exempt
def update_itinerary_with_preference(request):
    if request.method != "POST":
        raise SuspiciousOperation("POST Request only.")
    raise NotImplemented()
    json = FullItinerary.objects.filter(groupID=groupID)[0].encode()
    return JsonResponse(json)

@csrf_exempt
def update_itinerary_with_user(request):
    if request.method != "POST":
        raise SuspiciousOperation("POST Request only.")

    groupID = request.POST['groupID']

    email = request.POST['userEmail']
    name = request.POST['name']
    profileImageUrl = request.POST['profileImageUrl']
    new_traveller = get_or_create_user(groupID, email, name, profileImageUrl)

    itinerary = get_or_create_itinerary(groupID)
    itinerary.travellers.add(new_traveller)
    itinerary.save()

    return JsonResponse(itinerary.encode())

def get_or_create_itinerary(groupID):
    its = FullItinerary.objects.filter(groupID=groupID)
    if len(its) == 0:
        raise SuspiciousOperation("Call add itinerary first")
    else:
        return its[0]

def get_or_create_user(groupID, email, name, profileImageUrl):
    users = User.objects.filter(email=email)
    if len(users) > 0:
        return users[0]
    new_traveller = User(email=email, name=name, avatarImageUrl=profileImageUrl)
    new_traveller.save()

    return new_traveller

def get_itinerary(request):
    if request.method != "GET":
        raise SuspiciousOperation("GET Request only.")

    groupID = request.GET['groupID']
    json = FullItinerary.objects.filter(groupID=groupID)[0].encode()
    return JsonResponse(json)

@csrf_exempt
def add_itinerary(request):
    if request.method != "POST":
        raise SuspiciousOperation("POST Request only.")

    groupID = request.POST['groupID']
    tripName = request.POST['tripName']
    email = request.POST['userEmail']
    profileImageUrl = request.POST['profileImageUrl']
    name = request.POST['name']
    radius = request.POST['radius']
    location = request.POST['location']
    numDays = int(request.POST['numDays'])
    startDate = request.POST['startDate']
    createDate = request.POST['createDate']

    creator = None
    existing_user = User.objects.filter(email=email)
    if len(existing_user) <= 0:
        creator = User(email=email, name=name, avatarImageUrl=profileImageUrl)
        creator.save()
    else:
        creator = existing_user[0]

    query_itinerary = FullItinerary.objects.filter(groupID=groupID)
    if len(query_itinerary) <= 0:
        itinerary = FullItinerary(
            groupID=groupID,
            tripName=tripName,
            numDays=numDays,
            startDate=startDate,
            createDate=createDate,
            location=location,
            radius=radius)
        itinerary.save()
        itinerary.travellers.add(creator)
    else:
        itinerary = query_itinerary[0]

    # Collect initial places
    json = GooglePlacesAPIClient.textSearch(
        search_text='Attractions',
        location=itinerary.location,
        radius=itinerary.radius)
    attractions = Attraction.createAttractionsFromJSON(json, itinerary.groupID)

    # Handle photos
    for a in attractions:
        if len(a.rawPlaceDetails) == 0:
            # Make place details request
            placeDetailJSON = GooglePlacesAPIClient.placeDetails(placeid=a.placeID)
            a.rawPlaceDetails = placeDetailJSON
            assert "result" in placeDetailJSON
            photosresultJson = placeDetailJSON["result"]

            # Parse through all photos and request photo info for each.
            if "photos" in photosresultJson:
                photosJson = photosresultJson["photos"]
                for photo in photosJson:
                    ref = photo["photo_reference"]
                    url = GooglePlacesAPIClient.photosURL(photoreference=ref)
                    Photo.createFromJSON(url, a)
            a.save()

    return JsonResponse(itinerary.encode())

def remove_itinerary(request):
    return JsonResponse({"Status": "Unsupported"})
ACCESS_TOKENS = [
    "AIzaSyAx4plxTgzdDQKElwO6ZQdR1EmxTyUu4nw", # new
    "AIzaSyDQ0zLMHG20MOUjS7TuPIDrtXK9A64Zxug", # old
    "AIzaSyAMb_CXFPnuPJL5RUKwWxyooOx7K-JaCys", # oldest
]
ACCESS_TOKEN_INDEX = 0
ACCESS_TOKEN = os.environ['ACCESS_TOKEN']

class GooglePlacesAPIClient(object):

    def __init__(self):
        pass

    @classmethod
    def textSearch(self, search_text='', location='', radius=''):
        query_params = {
            "query": urllib.quote(search_text),
            "sensor": "false",
        }
        if len(location) > 0:
            query_params["location"] = location
        if len(radius) > 0:
            query_params["radius"] = radius
        base_url = "https://maps.googleapis.com/maps/api/place/textsearch/json"

        return self.buildURLAndRequest(base_url, query_params)

    @classmethod
    def placeDetails(self, placeid="ChIJN1t_tDeuEmsRUsoyG83frY4"):
        base_url = "https://maps.googleapis.com/maps/api/place/details/json"
        query_params = {
            "placeid": urllib.quote(placeid),
        }
        return self.buildURLAndRequest(base_url, query_params)

    @classmethod
    def photosURL(self, photoreference="CnRtAAAATLZNl354RwP_9UKbQ_5Psy40texXePv4oAlgP4qNEkdIrkyse7rPXYGd9D_Uj1rVsQdWT4oRz4QrYAJNpFX7rzqqMlZw2h2E2y5IKMUZ7ouD_SlcHxYq1yL4KbKUv3qtWgTK0A6QbGh87GB3sscrHRIQiG2RrmU_jF4tENr9wGS_YxoUSSDrYjWmrNfeEHSGSc3FyhNLlBU"):
        base_url = "https://maps.googleapis.com/maps/api/place/photo"
        query_params = {
            "photoreference" : photoreference,
            "maxwidth": "400",
        }
        return self.buildURL(base_url, query_params)

    @classmethod
    def buildURL(self, base_url, query_params={}):
        url = base_url
        url += '?key=' + ACCESS_TOKEN
        for key, value in query_params.iteritems():
            url += "&" + key + "=" + value
        return url

    @classmethod
    def buildURLAndRequest(self, base_url, query_params={}):
        url = self.buildURL(base_url, query_params)
        print "REQUEST: ", url
        response = requests.get(url)
        print "RESPONSE: ", response
        json = response.json()
        if json["status"] == "OVER_QUERY_LIMIT":
            ACCESS_TOKEN = ACCESS_TOKENS[index % len(ACCESS_TOKENS)]
            ACCESS_TOKEN_INDEX = ACCESS_TOKEN_INDEX + 1
            json = response.json()
            if json["status"] == "OVER_QUERY_LIMIT":
                raise SuspiciousOperation("Over Google query limit")
            else:
                return json
        return json

# All types supported by google
# From https://developers.google.com/places/supported_types
GOOGLE_PLACE_TYPES =  ["accounting", "airport", "amusement_park", "aquarium", "art_gallery",
    "atm", "bakery", "bank", "bar", "beauty_salon", "bicycle_store", "book_store",
    "bowling_alley", "bus_station", "cafe", "campground", "car_dealer", "car_rental",
    "car_repair", "car_wash", "casino", "cemetery", "church", "city_hall", "clothing_store",
    "convenience_store", "courthouse", "dentist", "department_store", "doctor", "electrician",
    "electronics_store", "embassy", "fire_station", "florist", "funeral_home", "furniture_store",
    "gas_station", "grocery_or_supermarket", "gym", "hair_care", "hardware_store",
    "hindu_temple", "home_goods_store", "hospital", "insurance_agency", "jewelry_store",
    "laundry", "lawyer", "library", "liquor_store", "local_government_office", "locksmith",
    "lodging", "meal_delivery", "meal_takeaway", "mosque", "movie_rental", "movie_theater",
    "moving_company", "museum", "night_club", "painter", "park", "parking", "pet_store",
    "pharmacy", "physiotherapist", "plumber", "police", "post_office", "real_estate_agency",
    "restaurant", "roofing_contractor", "rv_park", "school", "shoe_store", "shopping_mall",
    "spa", "stadium", "storage", "store", "subway_station", "synagogue", "taxi_stand",
    "train_station", "travel_agency", "university", "veterinary_care", "zoo"]


