import json

from datetime import datetime
from django.db.models import Q
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from .models import Message


def sendMessage(request):
    if request.method == 'POST':
        # XMLHttpRequest, not a Django request
        data = json.loads(request.body)

        body = data['body']
        receiverID = data['receiverID']

        if not receiverID:
            raise ValueError('Message must have a receiver.')
        elif not body:
            raise ValueError('Cannot send empty message.')

        receiver = User.objects.get(id=receiverID)

        message = Message(sender=request.user,
                          receiver=receiver,
                          body=body,
                          send_date=datetime.now())
        message.save()

        thread = Message.objects.filter((
                Q(sender=receiverID) & Q(receiver=request.user)) | (
                Q(sender=receiverID) & Q(receiver=request.user))).order_by('send_date')

        for msg in thread:
            msg.received = receiverID == request.user.id

        parms = {
            'thread': thread,
            'message': 'Message sent successfully!'
        }

        return redirect('/studenthome/')#render(request, 'messaging/message_thread.html', parms)
    else:
        raise NotImplementedError('Nothing to receive from this view.')
