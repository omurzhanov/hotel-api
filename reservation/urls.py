
from django.urls import path,include,re_path
from .views import *

urlpatterns = [
    path('guest/',api_guest_list_view,name='guest-objects'),
    path('booking/',api_booking_list_view,name='booking-objects')
]