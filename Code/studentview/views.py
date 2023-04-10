from django.shortcuts import get_object_or_404, render
from django.views import generic
from .models import ClassWaitlist
from django.contrib.auth.models import User, Group

# Create your views here.
classes = [
    {
        'classname': 'CSCI464-01',
        'professor': 'John DOe',
        'datetime':'MWF 11:00AM - 11:50AM',
        'CRN':'XXXXX',
        'waitlistposition':'3/25 in line'
    },
    {
        'classname': 'CSCI101-01',
        'professor': 'Janet DOe',
        'datetime':'MWF 10:00AM - 11:50AM',
        'CRN':'XXXX3',
        'waitlistposition':'4/25 in line'
    }
]

def home(request):
    context={
        'classes':classes
    }
    return render(request,'studentview/home.html', context)

def joinWaitlist(request):
    return render(request,'studentview/join_waitlist.html', {'title': 'join waitlist'})

class DetailView(generic.DetailView):
    model = ClassWaitlist
    
    template_name = 'studentview/detail.html'

# def detail(request, pk):
#     class_waitlist = get_object_or_404(ClassWaitlist)
#     return render(request, "studentview/detail.html", class_waitlist) 

