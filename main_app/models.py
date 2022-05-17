from django import forms
from django.db import models
from django.contrib.auth.models import User
import uuid
import datetime
import os

LOOKING_FOR = (
    ('MALE', 'Men'),
    ('FEMALE', 'Women'),
    ('BOTH', 'Both'),
)

ETHNICITY = (
    ('WHITE', 'White'),
    ('ASIAN: INDIAN', 'Asian: Indian'),
    ('ASIAN: PAKISTANI', 'Asian: Pakistani'),
    ('ASIAN: BANGLADESHI', 'Asian: Bangladeshi'),
    ('ASIAN: CHINESE', 'Asian: Chinese'),
    ('FILIPINO', 'FILIPINO'),
    ('BLACK', 'Black'),
    ('MIXED', 'Mixed'),
    ('OTHER ETHNICITY', 'Other Ethnicity')
)
RELATIONSHIP_TYPE = (
    ('RELATIONSHIP', 'relationship'),
    ('SOMETHING CASUAL', 'something casual'),
    ('DONT KNOW YET', 'dont know yet'),
    ('MARRIAGE', 'marriage')
)
KIDS = (
    ('WANT SOMEDAY', 'WANT SOMEDAY'),
    ('DO NOT WANT', 'do not want'),
    ('HAVE AND WANT MORE', 'have and want more'),
    ('HAVE AND DO NOT WANT MORE', 'have and do not want more'),
    ('NOT SURE YET', 'NOT SURE YET'),
)
GENDER = (
    ("MALE", "Male"),
    ("FEMALE", "Female"))

class Profile(models.Model):
    user = models.TextField(max_length=20, blank=False )
    bio = models.TextField(max_length=500, default='Tell us about yourself!', blank=False)
    gender = models.CharField(choices=GENDER, default=GENDER[0][0], max_length=20,)
    ethnicity = models.CharField(choices=ETHNICITY, default="WHITE", blank=False, max_length=20)
    relationship_type = models.CharField(choices=RELATIONSHIP_TYPE, default="DONT KNOW YET", blank=False, max_length=100)
    kids = models.CharField(choices=KIDS, default="NOT SURE YET", blank=False, max_length=100)
    height = models.DecimalField(max_digits=10, default=180.34, decimal_places=2)
    looking_for = models.CharField(choices=LOOKING_FOR, default='BOTH', blank=False, max_length=6)
    location = models.CharField(max_length=100, default='', blank=False)
    birth_date = models.DateField(null=True, default='1990-01-01', blank=True)

    def age(self):
        return int((datetime.date.today() - self.birth_date).days / 365.25  )

class Photo(models.Model):
  url = models.CharField(max_length=200)
  user = models.ForeignKey(Profile, on_delete=models.CASCADE)
  def __str__(self):
    return f'Photo for profile_id: {self.profile_id} at url: {self.url}'
