
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
import datetime

class Profile(models.Model):
    user = models.TextField(max_length=20, blank=False )
    bio = models.TextField(max_length=500, default='Tell us about yourself!', blank=False)
    gender = models.TextField(max_length=20,)
    ethnicity = models.TextField(default="WHITE", blank=False, max_length=20)
    relationship_type = models.TextField(default="DONT KNOW YET", blank=False, max_length=100)
    kids = models.TextField(default="NOT SURE YET", blank=False, max_length=100)
    height = models.DecimalField(max_digits=10, default=180.34, decimal_places=2)
    looking_for = models.TextField(default='BOTH', blank=False, max_length=6)
    location = models.TextField(max_length=100, default='', blank=False)
    birth_date = models.DateField(null=True, default='1990-01-01', blank=True)

    def age(self):
        return int((datetime.date.today() - self.birth_date).days / 365.25  )
    
    def get_absolute_url(self):
        return reverse('detail', kwargs={'profile_id': self.id})
        

class Photo(models.Model):
    url = models.CharField(max_length=200)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return f"Photo for profile_id: {self.profile_id} @{self.url}"