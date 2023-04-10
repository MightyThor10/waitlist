from django.shortcuts import get_object_or_404, render
from django.views import generic
from .models import ClassWaitlist, StudentTicket
from django.contrib.auth.models import User, Group

# Create your views here.


def home(request):

    currentUser = request.user
    groupOfUser = currentUser.groups.all().first()

    classes = []
    message =  ""

    if (not currentUser.is_anonymous):
        if (groupOfUser):
            if (groupOfUser.id == 1):
                classes = ClassWaitlist.objects.filter(professor=currentUser.pk)
            elif (groupOfUser.id == 2):
                studentTickets = StudentTicket.objects.filter(student=currentUser.pk)
                classPKs = set()
                for ticket in studentTickets:
                    classPKs.add(ticket.class_waitlist.pk)
                classPKs = list(classPKs)
                classes = ClassWaitlist.objects.filter(pk__in=classPKs)
        else:
            message = "You are not logged in as a professor or a student! This is a legacy account. Please make a new one"
    if (currentUser.is_anonymous):
        message = "Log in to view your classes!"
         

    context={
        'classes':classes,
        'message':message,
        'isProfessor':groupOfUser.id==1,
        'isStudent':groupOfUser.id==2
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

