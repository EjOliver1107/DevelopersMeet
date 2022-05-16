from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
import os
import uuid
import boto3
from .models import User, Photo

# Create your views here.

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

@login_required
def users_index(request):
    users = User.objects.all()
    return render(request, 'users/index.html', { 'users': users })

@login_required
def users_detail(request, user_id):
    user = User.objects.get(id=user_id)
    return render(request, 'users/detail.html', { 'user': user })
    

@login_required
def add_photo(request, user_id):
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        try:
            bucket = os.environ['S3_BUCKET']
            s3.upload_fileobj(photo_file, bucket, key)
            url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
            Photo.objects.create(url=url, user_id=user_id)
        except Exception as e:
            print('An error occurred uploading file to S3')
            print(e)
    return redirect('/users/', user_id=user_id)

def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('about')
    else:
      error_message = 'Invalid sign up - Try Again'
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)

