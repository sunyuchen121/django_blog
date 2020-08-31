

from django.urls import path
from userprofile import views
urlpatterns = [
    path('login/',views.UserLogin),
    path('register/',views.register),
    path('logout/',views.Userlogout)
]