from django.db import models
from django.urls import reverse
# from datetime import date

from django.contrib.auth.models import Profile

# profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

# class Profile(models.Model):
#     profile = models.OneToOneField(User, on_delete=models.CASCADE)
#     favorite_color = models.CharField(max_length=50)

class Profile(models.Model):

  # define the fields/columns
  name = models.CharField(max_length=100)
  age = models.IntegerField()
  location = models.CharField(max_length=100)
  occupation = models.CharField(max_length=100)
  bio = models.TextField(max_length=250)

  def __str__(self):
    return f'{self.name} ({self.id})'

  def get_absolute_url(self):

    return reverse('index', kwargs={'profile_id': self.id})

class Photo(models.Model):
  url = models.CharField(max_length=200)
  user = models.ForeignKey(Profile, on_delete=models.CASCADE)

  def __str__(self):
    return f'Photo for profile_id: {self.profile_id} at url: {self.url}'
