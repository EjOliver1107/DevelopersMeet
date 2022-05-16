from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.views.generic import ListView, DetailView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
import os
import uuid
import boto3

from .models import Profile, Photo




# Create your views here.

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

@login_required

def profile_index(request):
    profile = Profile.objects.all()
    return render(request, 'profile/index.html', { 'profile': profile })

@login_required
def profile_detail(request, profile_id):
    profile = Profile.objects.get(id=profile_id)
    return render(request, 'profile/detail.html', { 'profile': profile })
    

@login_required
def add_photo(request, profile_id):
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        try:
            bucket = os.environ['S3_BUCKET']
            s3.upload_fileobj(photo_file, bucket, key)
            url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
            Photo.objects.create(url=url, profile_id=profile_id)
        except Exception as e:
            print('An error occurred uploading file to S3')
            print(e)
    return redirect('/profile/', profile_id=profile_id)

def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():

      profile = form.save()
      login(request, profile)

      return redirect('about')
    else:
      error_message = 'Invalid sign up - Try Again'
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)


