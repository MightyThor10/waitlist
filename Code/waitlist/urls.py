from django.urls import path
from waitlist.views import waitlistHome

urlpatterns = [
    path("", waitlistHome, name="Waitlist"),
]
