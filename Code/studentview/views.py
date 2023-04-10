from django.shortcuts import get_object_or_404, render
from django.views import generic
from .models import ClassWaitlist, StudentTicket
from django.contrib.auth.models import User, Group

# Create your views here.


def home(request):

    currentUser = request.user
    groupOfUser = currentUser.groups.all().first()

    classes = [
            {
                'className': 'CSCI464-01',
                'professor': 'John DOe',
                'schedule':'MWF 11:00AM - 11:50AM',
                'crn':'XXXXX',
                'waitlistposition':'3/25 in line'
            },
            {
                'className': 'CSCI101-01',
                'professor': 'Janet DOe',
                'schedule':'MWF 10:00AM - 11:50AM',
                'crn':'XXXX3',
                'waitlistposition':'4/25 in line'
            }
        ]   

    if (not currentUser.is_anonymous):
        if (groupOfUser.id == 1):
            classes = ClassWaitlist.objects.filter(professor=currentUser.pk)
    # if (groupOfUser.id == 2):
    #     studentTickets = StudentTicket(student=currentUser.pk)
    #     print(studentTickets)
    #     #classes = ClassWaitlist(professor=currentUser.pk)
         

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

