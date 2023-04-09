from django.urls import path
from. import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='student-home'),
    path('joinwaitlist/',views.joinWaitlist, name='join-waitlist'),
    path("<int:pk>/detail/", views.DetailView.as_view(), name='detail')
]