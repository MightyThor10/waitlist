from django.db import models
from django.contrib.auth.models import User, Group

class ClassWaitlist(models.Model):
    className = models.CharField(max_length=200)
    classCode = models.CharField(max_length=200) #ex: CSCI425
    crn = models.IntegerField(default=0)
    schedule = models.CharField(max_length=200)
    sortType = models.CharField(max_length=200) #we should probably change this to an enum eventually
    term = models.CharField(max_length=200) #we should probably turn this into some kind of custom datatype eventually
    professor = models.ForeignKey(User, on_delete=models.CASCADE) #dunno if cascade is nessicary.
    date_added = models.DateTimeField("date published")

    def __str__(self):
        return self.className

class StudentTicket(models.Model):
    className = models.CharField(max_length=200) #may cut these
    studentName = models.CharField(max_length=200) #may cut these
    class_waitlist = models.ForeignKey(ClassWaitlist, on_delete=models.CASCADE) #dunno if cascade is nessicary.
    date_joined = models.DateTimeField("date joined")
    student = models.ForeignKey(User, on_delete=models.CASCADE) #dunno if cascade is nessicary.

    def __str__(self):
        return self.className + ' - ' + self.studentName + ' : ' + self.date_joined
