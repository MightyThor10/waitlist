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
    request_academic_status = models.BooleanField(default=False, verbose_name='Request Academic Status')
    request_major = models.BooleanField(default=False, verbose_name='Request Major')
    request_msg = models.BooleanField(default=False, verbose_name='Request Message')

    def __str__(self):
        return self.className



class StudentTicket(models.Model):
    class_waitlist = models.ForeignKey(ClassWaitlist, on_delete=models.CASCADE)
    date_joined = models.DateTimeField("date joined")
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    position = models.IntegerField(default=0)  # Add this line
    waitlist_status = models.CharField(max_length=1, default="p") #a = accept r = reject p = pending
    student_academic_status = models.CharField(max_length=20, verbose_name='Academic Status', default = '')
    student_major = models.CharField(max_length=100, verbose_name='Major', default='')
    msg = models.CharField(max_length=200, verbose_name='Message for Professor', default='')
    def __str__(self):
        return_msg = str(self.student) + " - " + str(self.student.email)
        if self.student_major != '':
            return_msg += " - " + str(self.student_major) + " Major"
        if self.student_academic_status != '':
            return_msg += " - " + str(self.student_academic_status)
        return return_msg + ' : ' + str(self.date_joined.strftime("%d/%m/%Y, %H:%M:%S"))
