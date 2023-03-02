from datetime import datetime

import django.utils
from django.db import models
from django.db.models import DateTimeField
from django.contrib.auth.models import User

TAGS = (
    (1, "sping"),
    (2, "winter"),
    (3, "summer"),
    (4, "autumn"),
    (5, "sea"),
    (6, "sun"),
)


LOCATIONS = (
    (1, "Warsaw"),
    (2, "London"),
    (3, "Gdansk"),
    (4, "Krakow"),
    (5, "Berlin"),
    (6, "Madrit"),
)


class Tag(models.Model):
    tag_name = models.CharField(max_length=256)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.tag_name



class Photo(models.Model):
    name = models.CharField(max_length=256, default="blank")
    photo = models.ImageField(upload_to='photos')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    # date_sent = models.DateTimeField(auto_now_add=True)
    # take_by = models.CharField(max_length=256)
    taken_date = DateTimeField(null=True, default=django.utils.timezone.now)
    tag = models.ManyToManyField(Tag)

    def __str__(self):
        return self.name





class Album(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    album_name = models.CharField(max_length=256)
    # album = models.ManyToManyField(Photo)

# class Location(models.Model):
#     location_name = models.CharField(max_length=256, choices=LOCATIONS)
#     location = models.ForeignKey(Photo, on_delete=models.CASCADE)


# class Camera(models.Model):
#     photo = models.OneToOneField(Photo, on_delete=models.CASCADE, primary_key=True)
#     camera_name = models.CharField(max_length=256)

class Display_photos(models.Model):
    display_photo = models.ImageField(upload_to='display_photos')





