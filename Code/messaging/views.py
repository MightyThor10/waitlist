import json

from datetime import datetime
from django.db.models import Q
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import redirect, render
from .models import Message


def readThread(request):
    if request.method == 'POST':
        # XMLHttpRequest, not a Django request
        data = json.loads(request.body)
        nameID = data['nameID']

        if not nameID:
            raise ValueError('Must have a thread to mark as read')

        # Populate the read_date field of all unread messages in thread
        thread_messages = Message.objects.filter(
            Q(read_date__isnull=True) & (Q(sender=nameID) | Q(receiver=nameID))
        )
        read_date = datetime.now()
        for msg in thread_messages:
            msg.read_date = read_date
            msg.save()

        return JsonResponse({ 'nameID': nameID}, status=201)
    else:
        raise NotImplementedError('Nothing to receive from this view.')



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

        thread = [{
            'thread': {
                'body': message.body,
                'received': receiverID == request.user.id
            }
        }]

        data = {
            'message_body': message.body,
            'receiverID': receiverID
        }

        return JsonResponse(data, status=201)
    else:
        raise NotImplementedError('Nothing to receive from this view.')
