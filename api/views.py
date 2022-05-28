from django.shortcuts import render
from rest_framework.response import Response
from .serializers import CitySerializer
from rest_framework.generics import RetrieveAPIView, ListAPIView
from api.models import CityClimate
from django.utils import timezone
from datetime import timedelta
from django.core.cache import caches
from .functions import update_or_make_city_detail

cache = caches.create_connection("default")


class CityDetail(RetrieveAPIView):
    queryset = CityClimate.objects.all()
    serializer_class = CitySerializer

    def get(self, request, **kwargs):
        city_name = request.GET.get("city_name")
        city_in_redis = cache.get(city_name)
        if city_in_redis is not None:  # city exist in redis
            print("massage : city exist in redis")
            return Response({
                'دما': city_in_redis
            })
        else:  # city doesnt exist in redis
            try:  # check the city is in database or not
                selected_city = CityClimate.objects.filter(city=city_name).last()
                temp_of_city = selected_city.temp
                if selected_city.last_update_time > timezone.now() - timedelta(
                        minutes=5):  # update time is not expired
                    print("massage : city is in database and is not expired")
                    cache.set(city_name, temp_of_city, 30)
                    serializer = CitySerializer(selected_city)
                    return Response({
                        'دما': serializer.data,
                    })
                else:  # update time is expired
                    jsonData = update_or_make_city_detail(city_name, selected_city)  # update
                    print("massage : city updated in database and put in redis")
                    return Response({
                        'دما': jsonData,
                    })

            except:  # the city is not in database
                try:  # the city is in main api
                    jsonData = update_or_make_city_detail(city_name, CityClimate())  # make new
                    print("massage : new city made in database and put in redis")
                    return Response({
                        'دما': jsonData,
                    })
                except:  # the city is not in main api=invalid city name
                    print("massage : no city like that")
                    return Response({
                        'نتیجه': 'شهری با نام وارد شده پیدا نشد',
                    })


class CityList(ListAPIView):
    queryset = CityClimate.objects.all()
    serializer_class = CitySerializer


def city_list(request):
    cities = CityClimate.objects.all()
    time = timezone.now()
    context = {
        'cities': cities,
        'time': time
    }
    return render(request, "api/city_list.html", context)
