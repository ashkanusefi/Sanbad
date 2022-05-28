from django.test import SimpleTestCase
from django.urls import reverse, resolve
from rest_framework.test import APITestCase, APIClient
from rest_framework import status


class CityDetailAPIViewTests(APITestCase):
    city_url = reverse("api:CityDetail") + "?city_name=" + "تهران"

    def test_get_city_detail(self):
        print(self.city_url)
        response = self.client.get(self.city_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
