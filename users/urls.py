from django.urls import path
from .views import *


urlpatterns = [
    path('', home2, name='users-home'),
    path('register/', RegisterView.as_view(), name='users-register'),
    path('profile/', profile, name='users-profile'),
    # path('login/', log, name='users-login'),
    path('readmore/',readmore),
    path('ngo_list/', ngo_list, name='ngo_list'),
    # path('contactus/',contactus),
    # path('aboutus/',aboutus),
    path('home/', home, name='home'),
    path('search/', search, name='search'),
    # path('search1/', search1, name='search1'),
    path('xyz/', xyz, name='xyz'),
   # path('pay/', pay, name='pay'),
    path('donate/', donate, name='donate'),
    path('success/', success, name='succes'),
]
