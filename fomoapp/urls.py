"""fomo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^test_google_places/$', views.testGooglePlaces, name='testGooglePlaces'),
    url(r'^get_recommendations/$', views.get_recommendations, name='get_recommendations'),
    url(r'^get_itinerary/$', views.get_itinerary, name='get_itinerary'),
    url(r'^get_itineraries_for_user/$', views.get_itineraries_for_user, name='get_itineraries_for_user'),
    url(r'^add_itinerary/$', views.add_itinerary, name='add_itinerary'),
    url(r'^update_itinerary_with_vote/$', views.update_itinerary_with_vote, name='update_itinerary_with_vote'),
    url(r'^update_itinerary_with_preference/$', views.update_itinerary_with_preference, name='update_itinerary_with_preference'),
    url(r'^update_itinerary_with_user/$', views.update_itinerary_with_user, name='update_itinerary_with_user'),
    url(r'^remove_itinerary/$', views.remove_itinerary, name='remove_itinerary'),

]
