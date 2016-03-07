from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, JsonResponse

import urllib
import requests
import os
from .models import Attraction


def index(request):
    return HttpResponse("Welcome to Fomo's home page! Feelings some fomo? Check out: https://github.com/jennify/Fomo")

def restaurants(request):
    json = GooglePlacesAPIClient.textSearch(search_text='Restaurants')
    Attraction.createAttractionsFromJSON(json,"FakeGroupID")
    # attractions =
    # for attraction in attractions:
    #     placeID = attraction["place_id"]
    #     a = Attraction(placeID=placeID, rawData=attraction, groupID="groupID")
    #     a.save()
    return JsonResponse({"results":json["results"]})

def placedetail(request):
    return JsonResponse(GooglePlacesAPIClient.placeDetails())

def get_recommendations(request):
    if request.method != "GET":
        raise Exception("GET Request only.")

    groupID = request.GET['groupID']
    email = request.GET['user_email']

    response = {}
    return JsonResponse({"Email": email})
    # return JsonResponse(GooglePlacesAPIClient.textSearch(search_text='Restaurants'))

def update_itinerary_with_vote(request):
    return JsonResponse({"Statue": "Incomplete"})

def update_itinerary_with_preference(request):
    return JsonResponse({"Statue": "Incomplete"})

def get_itinerary(request):
    return JsonResponse({"Statue": "Incomplete"})

def add_group(request):
    if request.method != "POST":
        raise Exception("POST Request only.")
        # , groupID, email, firstName, lastName, city
    groupID = request.POST['groupID']
    email = request.POST['email']

    return JsonResponse({"Email": email})

def update_group(request):
    return JsonResponse({"Statue": "Incomplete"})

def remove_group(request):
    return JsonResponse({"Statue": "Incomplete"})

def get_group(request):
    return JsonResponse({"Statue": "Incomplete"})

ACCESS_TOKEN = os.environ['ACCESS_TOKEN']

class GooglePlacesAPIClient(object):

    def __init__(self):
        pass

    @classmethod
    def textSearch(self, search_text=''):
        query_params = {
            "query": urllib.quote(search_text),
            "sensor": "false",
        }
        base_url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
        print(query_params)

        return self.buildURL(base_url, query_params)

    @classmethod
    def placeDetails(self, placeid="ChIJN1t_tDeuEmsRUsoyG83frY4"):
        base_url = "https://maps.googleapis.com/maps/api/place/details/json"
        query_params = {
            "placeid": urllib.quote(placeid),
        }
        return self.buildURL(base_url, query_params)

    @classmethod
    def photos(self, photoreference="CnRtAAAATLZNl354RwP_9UKbQ_5Psy40texXePv4oAlgP4qNEkdIrkyse7rPXYGd9D_Uj1rVsQdWT4oRz4QrYAJNpFX7rzqqMlZw2h2E2y5IKMUZ7ouD_SlcHxYq1yL4KbKUv3qtWgTK0A6QbGh87GB3sscrHRIQiG2RrmU_jF4tENr9wGS_YxoUSSDrYjWmrNfeEHSGSc3FyhNLlBU"):
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

        response = requests.get(url)
        return response.json()

# All types supported by google
# From https://developers.google.com/places/supported_types
GOOGLE_PLACE_TYPES =  ["accounting", "airport", "amusement_park", "aquarium", "art_gallery", "atm", "bakery", "bank", "bar", "beauty_salon", "bicycle_store", "book_store", "bowling_alley", "bus_station", "cafe", "campground", "car_dealer", "car_rental", "car_repair", "car_wash", "casino", "cemetery", "church", "city_hall", "clothing_store", "convenience_store", "courthouse", "dentist", "department_store", "doctor", "electrician", "electronics_store", "embassy", "fire_station", "florist", "funeral_home", "furniture_store", "gas_station", "grocery_or_supermarket", "gym", "hair_care", "hardware_store", "hindu_temple", "home_goods_store", "hospital", "insurance_agency", "jewelry_store", "laundry", "lawyer", "library", "liquor_store", "local_government_office", "locksmith", "lodging", "meal_delivery", "meal_takeaway", "mosque", "movie_rental", "movie_theater", "moving_company", "museum", "night_club", "painter", "park", "parking", "pet_store", "pharmacy", "physiotherapist", "plumber", "police", "post_office", "real_estate_agency", "restaurant", "roofing_contractor", "rv_park", "school", "shoe_store", "shopping_mall", "spa", "stadium", "storage", "store", "subway_station", "synagogue", "taxi_stand", "train_station", "travel_agency", "university", "veterinary_care", "zoo"]


