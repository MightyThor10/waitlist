from django.db import models
from django.contrib.auth.models import User, Group

class ClassWaitlist(models.Model):
    className = models.CharField(max_length=200, name="className")
    classCode = models.CharField(max_length=200) 
    crn = models.IntegerField(default=0)
    schedule = models.CharField(max_length=200)
    sortType = models.CharField(max_length=200)
    term = models.CharField(max_length=200)
    professor = models.ForeignKey(User, on_delete=models.CASCADE)
    date_added = models.DateTimeField("date published")
    closed = models.BooleanField(default=False)  # Add this line

    def __str__(self):
        return self.className



class StudentTicket(models.Model):
    class_waitlist = models.ForeignKey(ClassWaitlist, on_delete=models.CASCADE) #dunno if cascade is nessicary.
    date_joined = models.DateTimeField("date joined")
    student = models.ForeignKey(User, on_delete=models.CASCADE) #dunno if cascade is nessicary.

    def __str__(self):
        return str(self.class_waitlist) + ' - ' + str(self.student) + ' : ' + str(self.date_joined)
