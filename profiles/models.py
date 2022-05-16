from django.db import models
from django.contrib.auth.models import User
# from chat.models import Conversations
# from checkout.models import Subscription
from django.db.models.signals import post_save, pre_delete
from django.utils.crypto import get_random_string
from django.core.validators import MaxValueValidator, MinValueValidator
import uuid
import datetime
import os
import math
from django.db.models.expressions import RawSQL
from django.db.backends.signals import connection_created
from django.dispatch import receiver
import os

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, default='', blank=False)
    HAIR_COLOUR = (
        ('BLACK', 'Black'),
        ('BLONDE', 'Blonde'),
        ('BROWN', 'Brown'),
        ('RED', 'Red'),
        ('GREY', 'Grey'),
        ('BALD', 'Bald'),
        ('BLUE', 'Blue'),
        ('PINK', 'Pink'),
        ('GREEN', 'Green'),
        ('PURPLE', 'Purple'),
        ('OTHER', 'Other'),
    )
    BODY_TYPE = (
        ('THIN', 'Thin'),
        ('AVERAGE', 'Average'),
        ('FIT', 'Fit'),
        ('MUSCULAR', 'Muscular'),
        ('A LITTLE EXTRA', 'A Little Extra'),
        ('CURVY', 'Curvy'),
    )
    LOOKING_FOR = (
        ('MALE', 'Men'),
        ('FEMALE', 'Women'),
        ('BOTH', 'Both'),
    )
    APPROVAL = (
        ('TO BE APPROVED', 'To be approved'),
        ('APPROVED', 'Approved'),
        ('NOT APPROVED', 'Not approved')
    )
    
    HAIR_LENGTH = (
        ('LONG', 'Long'),
        ('SHOULDER LENGTH', 'Shoulder Length'),
        ('AVERAGE', 'Average'),
        ('SHORT', 'Short'),
        ('SHAVED', 'Shaved')
    )
    ETHNICITY = (
        ('WHITE', 'White'),
        ('ASIAN: INDIAN', 'Asian: Indian'),
        ('ASIAN: PAKISTANI', 'Asian: Pakistani'),
        ('ASIAN: BANGLADESHI', 'Asian: Bangladeshi'),
        ('ASIAN: CHINESE', 'Asian: Chinese'),
        ('BLACK', 'Black'),
        ('MIXED', 'Mixed'),
        ('OTHER ETHNICITY', 'Other Ethnicity')
    )
    RELATIONSHIP_STATUS = (
        ('NEVER MARRIED', 'Never Married'),
        ('DIVORCED', 'Divorced'),
        ('WIDOWED', 'Widowed'),
        ('SEPARATED', 'Separated')
    )
    EDUCATION = (
    ('HIGH SCHOOL', 'High School'),
    ('COLLEGE', 'College'),
    ('BACHELORS DEGREE', 'Bachelors Degree'),
    ('MASTERS', 'Masters'),
    ('PHD / POST DOCTORAL', 'PhD / Post Doctoral'),
    )
    GENDER = (
        ("MALE", "Male"),
        ("FEMALE", "Female"))

    gender = models.CharField(choices=GENDER, default="MALE", max_length=6)
    hair_length = models.CharField(choices=HAIR_LENGTH, default="LONG", blank=False, max_length=100)
    ethnicity = models.CharField(choices=ETHNICITY, default="WHITE", blank=False, max_length=100)
    relationship_status = models.CharField(choices=RELATIONSHIP_STATUS, default="NEVER MARRIED", blank=False, max_length=100)
    education = models.CharField(choices=EDUCATION, default="HIGH SCHOOL", blank=False, max_length=100)
    height = models.DecimalField(max_digits=10, default=180.34, decimal_places=2)
    hair_colour = models.CharField(choices=HAIR_COLOUR, default="BLACK", blank=False, max_length=10)
    body_type = models.CharField(choices=BODY_TYPE, default="AVERAGE", blank=False, max_length=15)
    looking_for = models.CharField(choices=LOOKING_FOR, default='BOTH', blank=False, max_length=6)
    children = models.BooleanField(default=False)
    location = models.CharField(max_length=100, default='', blank=False)
    citylat = models.DecimalField(max_digits=9, decimal_places=6, default='-2.0180319')
    citylong = models.DecimalField(max_digits=9, decimal_places=6, default='52.5525525')
    birth_date = models.DateField(null=True, default='1990-01-01', blank=True)
    is_premium = models.BooleanField(default=False)
    is_verified = models.CharField(choices=APPROVAL, default="TO BE APPROVED", blank=False, max_length=14)

    def age(self):
        return int((datetime.date.today() - self.birth_date).days / 365.25  )
