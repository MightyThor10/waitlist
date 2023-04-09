from django.urls import path
from. import views

urlpatterns = [
    path('', views.home, name='student-home'),
    path('joinwaitlist/',views.joinWaitlist, name='join-waitlist'),
]