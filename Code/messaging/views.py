import json

from datetime import datetime
from django.db.models import Q
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from .models import Message

from users.models import StudentProfile


def buildInboxThread(message, nameID, unread):
    # nameID should be sender or receiver
    #     -> whichever is not the curUser
    thread = []

    thread_userObj = User.objects.get(id=nameID)
    if thread_userObj.groups.all().first() == 2:
        thread_user_pref_name = StudentProfile.objects.get(id=nameID).preferred_name
    else:
        thread_user_pref_name = thread_userObj.get_full_name()

    message_snippet = (message.body[:60] + '...') if len(message.body) > 75 else message.body

    entry_dict = {
        'name': thread_user_pref_name,
        'nameID': nameID,
        'message_snippet': message_snippet,
        'last_received': message.getInboxDate(),
        'unread': unread,
        'thread': thread
    }
    return render_to_string('messaging/inbox_thread.html', {
               'thread': entry_dict
           })


def readThread(request):
    if request.method == 'POST':
        # XMLHttpRequest, not a Django request
        data = json.loads(request.body)
        nameID = data['nameID']

        if not nameID:
            raise ValueError('Must have a thread to mark as read')

        # Populate the read_date field of all unread messages in thread
        thread_messages = Message.objects.filter(
            (Q(sender=nameID) | Q(receiver=nameID)) & Q(read_date__isnull=True)
        )
        read_date = datetime.now()
        for msg in thread_messages:
            msg.read_date = read_date
            msg.save()

        return JsonResponse({ 'nameID': nameID,
                              'read_count': thread_messages.count()
                            }, status=201)

    elif request.method == 'GET':
        unread_count = int(request.GET.get('unread_count'))

        if unread_count is None:
            return HttpResponseBadRequest()

        # Populate the read_date field of all unread messages in thread
        unread_messages = Message.objects.filter(
            Q(receiver=request.user) & Q(read_date__isnull=True)
        ).order_by('send_date')

        new_messages_count = unread_messages.count() - unread_count
        if new_messages_count == 0:
            return JsonResponse({ 'up-to-date': True }, status=201)
        elif new_messages_count > 0:
            # New messages since client reloaded
            new_messages = unread_messages[:new_messages_count]
            data = []
            new_inbox_nameIDs = set(new_messages.values_list('sender', flat=True))

            for senderID in new_inbox_nameIDs:
                thread = []
                inbox_msg = unread_messages.filter(Q(sender=senderID)).latest('send_date')
                conversation = Message.objects.filter(
                    (Q(sender=senderID) & Q(receiver=request.user)) |
                    (Q(sender=request.user) & Q(receiver=senderID))
                ).order_by('send_date')

                for msg in conversation:
                    thread.append({
                        'received': msg.receiver == request.user,
                        'body': msg.body,
                        'send_date': msg.send_date,
                        'read_date': msg.read_date
                    })

                data.append({
                    'nameID': senderID,
                    'unread_count': unread_messages.filter(Q(sender=senderID)).count(),
                    'inbox_thread_html': buildInboxThread(inbox_msg, senderID, True),
                    'thread_html': render_to_string('messaging/message_thread.html', {
                                        'thread': { 'thread':  thread }
                                    })
                })

            return JsonResponse({
                    'inbox_threads': data,
                    'up-to-date': False,
                    'new_unread_count': new_messages_count
                }, status=201)
        else:
            # Client interference: more unread messages than the server
            return HttpResponseBadRequest()

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

        data = {
            'inbox_thread_html': buildInboxThread(message, receiverID, False),
            'message_body': message.body,
            'receiverID': receiverID,
            'preferred_name': receiver.get_full_name(),# Should add preferred name
        }

        return JsonResponse(data, status=201)
    else:
        raise NotImplementedError('Nothing to receive from this view.')
