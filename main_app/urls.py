from django.urls import path
from . import views
#path > defines each route

#area where we define urls
urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),

    path('profile/', views.profile_index, name='index'),
    path('accounts/signup/', views.signup, name="signup"),
    path('users/<int:user_id>/add_photo/', views.add_photo, name='add_photo'),
    

]