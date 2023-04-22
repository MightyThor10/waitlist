from django.shortcuts import get_object_or_404, render, redirect
from django.views import generic
from .models import ClassWaitlist, StudentTicket
from django.contrib.auth.models import User, Group
from django.utils import timezone

# Create your views here.


def home(request):

    currentUser = request.user
    groupOfUser = currentUser.groups.all().first() #if we ever add more groups than profs and students, change this

    classes = []
    message =  ""
    isProfessor = False
    isStudent = False

    if (not currentUser.is_anonymous):
        if (groupOfUser):
            if (groupOfUser.id == 1):
                classes = ClassWaitlist.objects.filter(professor=currentUser.pk)
                isProfessor = True
            elif (groupOfUser.id == 2):
                isStudent = True
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
        'isProfessor':isProfessor,
        'isStudent':isStudent
    }
    return render(request,'studentview/home.html', context)

def joinWaitlist(request):

    if request.method =='POST':
        # TODO: Add error checking here, this currently has none lol
        classid = request.POST['classID']
        waitlist = ClassWaitlist.objects.get(id=classid)
        user = request.user
        if waitlist and user:
            st = StudentTicket.objects.create(class_waitlist=waitlist, date_joined= timezone.now(), student=user)
        response = redirect('/studenthome/')
        return response
    else:
        classes = ClassWaitlist.objects.all()

        context = {
            'title': 'join waitlist',
            'classes': classes
            }

        return render(request,'studentview/join_waitlist.html', context)
    
def createWaitlist(request):

    if request.method =='POST':
        name = request.POST['className']
        code = request.POST['classCode']
        crn = request.POST['classCRN']
        schedule = request.POST['classSchedule']
        sortType = request.POST['classSort']
        term = request.POST['classTerm']
        datePosted = timezone.now()
        user = request.user
        # StudentTicket.objects.create(class_waitlist=waitlist, date_joined= timezone.now(), student=user)
        
        cwl = ClassWaitlist.objects.create(className=name, classCode=code, crn=crn, schedule=schedule, sortType=sortType, term=term, date_added=datePosted, professor=user)
        
        response = redirect('/studenthome/')
        return response

    else:
        context = {
            'title': 'join waitlist'
            }
        return render(request,'studentview/create_class.html', context)

def removeFromWaitlist(request,waitlist_id):
    currentUser = request.user
    print("current user is"+ str(currentUser.pk))
    ticket = StudentTicket.objects.get(student_id=currentUser.pk,class_waitlist_id=waitlist_id)
    ticket.delete()
    return redirect('student-home')

class DetailView(generic.DetailView):
    model = ClassWaitlist
    
    template_name = 'studentview/detail.html'

# def detail(request, pk):
#     class_waitlist = get_object_or_404(ClassWaitlist)
#     return render(request, "studentview/detail.html", class_waitlist) 


