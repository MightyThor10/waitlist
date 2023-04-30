from django.urls import path
from. import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.home, name='student-home'),
    path('joinwaitlist/',views.joinWaitlist, name='join-waitlist'),
    path('leavewaitlist/', views.leaveWaitlist, name='leave_waitlist'),
    path('createclass/',views.createWaitlist, name='create-class'),
    path("<int:pk>/detail/", views.DetailView.as_view(), name='detail'),
    path("<int:pk>/edit/", views.EditView.as_view(), name='edit_waitlist'),
    path('closeclass/', views.close_class, name='close_class'),
    path('move_student/<int:ticket_id>/<str:direction>/', views.move_student, name='move_student'),
    path('update_waitlist_status/<int:ticket_id>/<str:newstatus>/', views.update_waitlist_status, name='update_waitlist_status'),
    path('leaveallwaitlists/', views.leave_all_waitlists, name='leave_all_waitlists'),
    path('archive/',views.archive, name='waitlist-archive'),
    path('archive_class/<int:class_id>', views.archive_class, name='archive_class'),
    path('unarchive_class/<int:class_id>', views.unarchive_class, name='unarchive_class'),
    path('sort_waitlist/<int:pk>/<str:sortType>/', views.sort_waitlist, name='sort_waitlist'),
]