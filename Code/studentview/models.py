from django.db import models
from django.contrib.auth.models import User, Group
from datetime import datetime

class ClassWaitlist(models.Model):
    className = models.CharField(max_length=200, name="className", verbose_name='Class Name')
    classDescription = models.TextField(verbose_name='Description', default=' ')
    classCode = models.CharField(max_length=200, verbose_name='Class Code') 
    crn = models.IntegerField(default=0, verbose_name='CRN')
    schedule = models.CharField(max_length=200, verbose_name='Schedule')
    sortType = models.CharField(max_length=200, verbose_name='Sort Type')
    term = models.CharField(max_length=200, verbose_name='Term')
    professor = models.ForeignKey(User, on_delete=models.CASCADE)
    date_added = models.DateTimeField("date published")
    closed = models.BooleanField(default=False)  # Add this line
    anonymous_waitlist = models.BooleanField(default=False, verbose_name='Anonymous Waitlist')

    def __str__(self):
        return self.className



class StudentTicket(models.Model):
    class_waitlist = models.ForeignKey(ClassWaitlist, on_delete=models.CASCADE)
    date_joined = models.DateTimeField("date joined")
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    position = models.IntegerField(default=0)  # Add this line
    waitlist_status = models.CharField(max_length=1, default="p" ) #a = accept r = reject p = pending
    msg = models.CharField(max_length=200, verbose_name='Message for Professor', default='')
    def __str__(self):
        return str(self.student) + " - " + str(self.student.email) + ' : ' + str(self.date_joined.strftime("%d/%m/%Y, %H:%M:%S"))


class WaitlistForm(models.Model):
    name = models.CharField(max_length=100, blank=True, verbose_name='Name')
    academic_status = models.CharField(max_length=20, blank=True, verbose_name='Academic Status')
    major = models.CharField(max_length=100, blank=True, verbose_name='Major')
    msg = models.CharField(max_length=200, verbose_name='Message for Professor')