from django.db import models


class CityClimate(models.Model):
    city = models.CharField("نام شهر", max_length=60)
    temp = models.FloatField("دمای شهر", null=True, blank=True)
    last_update_time = models.DateTimeField("تاریخ اخرین بروز رسانی دما", auto_now=True)

    def __str__(self):
        return self.city
