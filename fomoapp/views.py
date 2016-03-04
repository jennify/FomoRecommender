from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, JsonResponse

import urllib
import requests
import os

def index(request):
    return HttpResponse("Hello, world. You're at the fomo's home page!")

def restaurants(request):
    # TODO(jlee): DON"T CHECK IN THIS CODE
    json = GooglePlacesAPIClient.textSearch(search_text='Restaurants')
    return JsonResponse(json)

def placedetail(request):
    return JsonResponse(GooglePlacesAPIClient.placeDetails())

ACCESS_TOKEN = os.environ['ACCESS_TOKEN']

class GooglePlacesAPIClient(object):

    def __init__(self):
        pass

    @classmethod
    def textSearch(self, search_text=''):
        query_params = {
            "query": urllib.quote(search_text),
            "sensor": "false",
            # "types": "",
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
    def buildURL(self, base_url, query_params={}):
        url = base_url
        url += '?key=' + ACCESS_TOKEN
        for key, value in query_params.iteritems():
            url += "&" + key + "=" + value

        response = requests.get(url)
        return response.json()

# Place details
# 'https://maps.googleapis.com/maps/api/place/details/json?placeid=ChIJN1t_tDeuEmsRUsoyG83frY4&key=YOUR_API_KEY'
# Photos
# https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference=CnRtAAAATLZNl354RwP_9UKbQ_5Psy40texXePv4oAlgP4qNEkdIrkyse7rPXYGd9D_Uj1rVsQdWT4oRz4QrYAJNpFX7rzqqMlZw2h2E2y5IKMUZ7ouD_SlcHxYq1yL4KbKUv3qtWgTK0A6QbGh87GB3sscrHRIQiG2RrmU_jF4tENr9wGS_YxoUSSDrYjWmrNfeEHSGSc3FyhNLlBU&key=YOUR_API_KEY

