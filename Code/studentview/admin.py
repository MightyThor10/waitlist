from django.contrib import admin

from .models import StudentTicket, ClassWaitlist

admin.site.register(ClassWaitlist)
admin.site.register(StudentTicket)
