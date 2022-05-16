from django.urls import path
from . import views
#path > defines each route

#area where we define urls
urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('profiles/', views.profile_index, name='index'),
    path('profiles/<int:profile_id>/', views.profile_detail, name='detail'),
    path('accounts/signup/', views.signup, name="signup"),
    path('profiles/<int:profile_id>/add_photo/', views.add_photo, name='add_photo'),
    

]