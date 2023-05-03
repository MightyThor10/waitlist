from django import forms
from django.contrib.auth.models import User
from .models import Message


class MessageForm(forms.ModelForm):
    RECIPIENT_PLACEHOLDER = (None, "Select recipient...")

    # Constructor for replied messages (no recipient choicefield)
    def __init__(self, sender=None, recipient=None, users=None, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)

        if sender is None:
            raise ValueError('There must be a sender to send a message.')
        if recipient is None:
            raise SyntaxError('To compose a new message, use the other constructor.')

        self.fields['sender'] = sender.id

        self.fields['body'].widget.attrs.update({
            'rows': 5, 'cols': 50,
            'placeholder': 'Send message...',
        })

    # Constructor for composed messages (recipient choicefield)
    def __init__(self, sender=None, users=None, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)

        if sender is None:
            raise ValueError('There must be a sender to send a message.')

        self.fields['sender'] = sender.id

        if len(users):
            self.fields['receiver'].choices = users
            self.fields['receiver'].choices.insert(0, self.RECIPIENT_PLACEHOLDER)
        else:
            self.fields['receiver'].choices = [self.RECIPIENT_PLACEHOLDER]

        self.fields['body'].widget.attrs.update({
            'rows': 5, 'cols': 50,
            'placeholder': 'Send message...',
        })
        self.fields['receiver'].widget.attrs.update({
            'id': 'compose-input-user',
            'class': 'form-select'})

    class Meta:
        model = Message
        fields = ['sender', 'receiver', 'body']
