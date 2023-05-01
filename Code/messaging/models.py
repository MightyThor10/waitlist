import datetime
import calendar

from django.contrib.auth.models import User
from django.db import models

from users.models import StudentProfile


class Message(models.Model):
    """
        Private messaging model
    """
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='sender_messages',
        verbose_name='Sender')

    receiver = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='receiver_messages',
        verbose_name='Recipient')

    body = models.TextField(verbose_name='Body')

    send_date = models.DateTimeField(verbose_name='sent at', auto_now_add=True)
    read_date = models.DateTimeField(verbose_name='read at', null=True, blank=True)

    def __str__(self):
        return 'Message from %s to %s at %s' % (
                self.sender.get_full_name(),
                self.receiver.get_full_name(),
                str(self.send_date.strftime("%d/%m/%Y, %H:%M:%S")))

    def getPreferredName(self, user):
            try:
                return StudentProfile.objects.get(user=user).preferred_name
            except StudentProfile.DoesNotExist:
                return user.get_full_name()

    def getInboxDate(self):
        now = datetime.datetime.now(datetime.timezone.utc)

        if (self.send_date - now).days < 1:
            return "{:d}:{:02d}".format(self.send_date.hour, self.send_date.minute)
        elif (self.send_date - now).days < 2:
            return 'Yesterday'
        elif (self.send_date - now).days < 7:
            return calendar.day_name[datetime.date(self.send_date).weekday()]
        else:
            return datetime.date.strftime(self.send_date, "%m/%d/%Y")
