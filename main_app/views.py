from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import uuid
import boto3
import os

from .models import Profile, Photo
from .forms import CommentForm





# Create your views here.

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

@login_required
def profile_index(request):
    profiles = Profile.objects.all()
    return render(request, 'profiles/index.html', { 'profiles': profiles })

@login_required
def profile_detail(request, profile_id):
    profile = Profile.objects.get(id=profile_id)
    comment_form = CommentForm(initial={
        'user': request.user
    }) 
    comments = profile.comment_set.all().values_list('id')
    return render(request, 'profiles/detail.html', {
         'profile': profile,
         'comment_form': comment_form,
         'comments': comments
         })

@login_required
def my_profile(request):
    profile = Profile.objects.get(user=request.user)
    return render(request, 'profiles/detail.html', {
        'profile': profile
    })
    
class ProfileCreate(LoginRequiredMixin, CreateView):
    model = Profile
    fields = ['bio', 'gender', 'ethnicity', 'relationship_type', 'kids', 'height', 'looking_for', 'location', 'birth_date']
    def form_valid(self,form):
        form.instance.user = self.request.user
        return super().form_valid(form)
       

class ProfileUpdate(LoginRequiredMixin, UpdateView):
    model = Profile
    fields = ['bio', 'gender', 'ethnicity', 'relationship_type', 'kids', 'looking_for', 'location']

class ProfileDelete(LoginRequiredMixin, DeleteView):
    model = Profile
    success_url = '/profiles/'


@login_required
def add_comment(request, profile_id):
  form = CommentForm(request.POST, initial={
      'user': request.user.id
  })
  print(form.errors)
  if form.is_valid():
    profile = Profile.objects.get(id = profile_id)
    new_comment = form.save(commit=False)
    new_comment.profile = profile
    # print('new_comment')
    new_comment.save()
  return redirect('detail', profile_id=profile_id)

@login_required
def add_photo(request):
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        try:
            bucket = os.environ['S3_BUCKET']
            s3.upload_fileobj(photo_file, bucket, key)
            url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
            Photo.objects.create(url=url, profile_id=request.user.profile.id)
        except Exception as e:
          print('An error occurred uploading file to S3')
          print(e)
    return redirect('detail', profile_id=request.user.profile.id)

def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():

      user = form.save()
      login(request, user)

      return redirect('index')
    else:
      error_message = 'Invalid sign up - Try Again'
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)


