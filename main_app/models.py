from django.db import models
from django.contrib.auth.models import User
# Create your models here.
user = models.ForeignKey(User, on_delete=models.CASCADE)