from django.shortcuts import render
from .models import Message


def sendMessage(request):
    if request.method == 'POST':
        receiverID = request.POST['receiver']
        body = request.POST['body']

        if not receiverID:
            raise ValueError('Message must have a receiver.')
        elif not body:
            raise ValueError('Cannot send empty message.')

        message = Message(sender=request.user, receiver=receiverID, body=body)
        print(message)
        message.save()
    else:
        raise NotImplementedError('Nothing to receive from this view.')
