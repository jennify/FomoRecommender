from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, JsonResponse



def index(request):
    return HttpResponse("Hello, world. You're at the fomo's home page!")


def test(request):
	return JsonResponse({"Hello":"world"})