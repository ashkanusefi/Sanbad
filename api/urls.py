from django.urls import path
from .views import CityDetail, CityList

app_name = "api"

urlpatterns = [
    path('city-details/', CityDetail.as_view(), name="CityDetail"),
    path('list_of_cities/', CityList.as_view(), name="CityList")

]
