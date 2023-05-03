import json

from datetime import datetime
from django.db.models import Q
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from .models import Message

from users.models import StudentProfile


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

        return JsonResponse({ 'nameID': nameID,
                              'read_count': thread_messages.count()
                            }, status=201)
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


        thread = []

        thread_userObj = User.objects.get(id=receiverID)
        if thread_userObj.groups.all().first() == 2:
            thread_user_pref_name = StudentProfile.objects.get(id=receiverID).preferred_name
        else:
            thread_user_pref_name = thread_userObj.get_full_name()

        message_snippet = (message.body[:60] + '...') if len(message.body) > 75 else message.body

        entry_dict = {
            'name': thread_user_pref_name,
            'nameID': receiverID,
            'message_snippet': message_snippet,
            'last_received': message.getInboxDate(),
            'unread': False,
            'thread': thread
        }
        inbox_thread_html = render_to_string('messaging/inbox_thread.html', {
            'thread': entry_dict
        })

        data = {
            'inbox_thread_html': inbox_thread_html,
            'message_body': message.body,
            'receiverID': receiverID
        }

        return JsonResponse(data, status=201)
    else:
        raise NotImplementedError('Nothing to receive from this view.')
