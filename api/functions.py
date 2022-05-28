from django.core.cache import caches
import requests

cache = caches.create_connection("default")


def update_or_make_city_detail(city_name, city_model):
    response = requests.get(
        "https://one-api.ir/weather/?token=544995:628b372224b131.55086726&action=now&city=" + city_name)  # call main API
    jsonData = response.json()["result"]['main']['temp']  # filter temperature in json data
    cache.set(city_name, jsonData, 30)
    city_model.city = city_name
    city_model.temp = jsonData
    city_model.save()
    return jsonData
