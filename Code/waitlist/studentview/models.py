from django.db import models
from django.contrib.auth.models import User, Group

class ClassWaitlist(models.Model):
    className = models.CharField(max_length=200, name='className', db_column='class_name')
    classCode = models.CharField(max_length=200, db_column='class_code') #ex: CSCI425
    crn = models.IntegerField(default=0)
    schedule = models.CharField(max_length=200)
    sortType = models.CharField(max_length=200, db_column='sort_type') #we should probably change this to an enum eventually
    term = models.CharField(max_length=200) #we should probably turn this into some kind of custom datatype eventually
    professor = models.ForeignKey(User, on_delete=models.CASCADE) #dunno if cascade is nessicary.
    date_added = models.DateTimeField("date published")

    class Meta:
        db_table = 'class_waitlist'

    def __str__(self):
        return self.className



class StudentTicket(models.Model):
    class_waitlist = models.ForeignKey(ClassWaitlist, on_delete=models.CASCADE) #dunno if cascade is nessicary.
    date_joined = models.DateTimeField("date joined")
    student = models.ForeignKey(User, on_delete=models.CASCADE) #dunno if cascade is nessicary.

    class Meta:
        db_table = 'student_ticket'

    def __str__(self):
        return str(self.class_waitlist) + ' - ' + str(self.student) + ' : ' + str(self.date_joined)
