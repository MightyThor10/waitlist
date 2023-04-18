from django.shortcuts import get_object_or_404, render, redirect
from django.views import generic
from .models import ClassWaitlist, StudentTicket
from django.contrib.auth.models import User, Group
from django.utils import timezone
from django.contrib import messages

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
        classid = request.POST['classID']
        user = request.user
        message = ""

        waitlist = ClassWaitlist.objects.filter(id=classid).first()

        if waitlist and user:
            existing_ticket = StudentTicket.objects.filter(class_waitlist=waitlist, student=user).first()
            if existing_ticket:
                message = "You have already joined this class's waitlist."
            else:
                last_position = StudentTicket.objects.filter(class_waitlist=waitlist).order_by('-position').first()
                new_position = last_position.position + 1 if last_position else 1
                st = StudentTicket.objects.create(class_waitlist=waitlist, date_joined=timezone.now(), student=user, position=new_position)
                response = redirect('/studenthome/')
                return response
        else:
            message = "The specified class does not exist."

        context = {
            'title': 'join waitlist',
            'message': message,
            'classes': ClassWaitlist.objects.all(),
        }
        return render(request, 'studentview/join_waitlist.html', context)

    else:
        classes = ClassWaitlist.objects.all()

        context = {
            'title': 'join waitlist',
            'classes': classes
        }
        return render(request, 'studentview/join_waitlist.html', context)


    

def leaveWaitlist(request):
    if request.method == 'POST':
        classid = request.POST['classID']
        user = request.user
        message = ""

        if user:
            existing_ticket = StudentTicket.objects.filter(class_waitlist_id=classid, student=user).first()
            if existing_ticket:
                existing_ticket.delete()
                response = redirect('/studenthome/')
                return response
            else:
                message = "You are not on this class's waitlist."
        else:
            message = "Invalid user."

        context = {
            'title': 'leave waitlist',
            'message': message,
            'classes': ClassWaitlist.objects.all(),
        }
        return render(request, 'studentview/leave_waitlist.html', context)

    else:
        classes = ClassWaitlist.objects.all()

        context = {
            'title': 'leave waitlist',
            'classes': classes
        }
        return render(request, 'studentview/leave_waitlist.html', context)


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



def close_class(request):
    if request.method == 'POST':
        class_id = request.POST['classID']
        user = request.user
        group_of_user = user.groups.all().first()
        is_professor = group_of_user and group_of_user.id == 1

        if not is_professor:
            return redirect('/studenthome/')

        try:
            class_to_delete = ClassWaitlist.objects.get(id=class_id, professor=user)
            class_to_delete.delete()
            messages.success(request, 'The class has been successfully deleted.')
        except ClassWaitlist.DoesNotExist:
            messages.error(request, 'The class does not exist or you did not create it.')

        return redirect('/studenthome/')

    return render(request, 'studentview/close_class.html')

class DetailView(generic.DetailView):
    model = ClassWaitlist
    template_name = 'studentview/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['isProfessor'] = self.request.user.groups.filter(name='Professor').exists()
        return context

# def detail(request, pk):
#     class_waitlist = get_object_or_404(ClassWaitlist)
#     return render(request, "studentview/detail.html", class_waitlist) 

def move_student(request, ticket_id, direction):
    ticket = get_object_or_404(StudentTicket, id=ticket_id)
    if not request.user == ticket.class_waitlist.professor:
        return redirect('/studenthome/')
    if direction == "up":
        if ticket.position > 1:
            other_ticket = StudentTicket.objects.get(
                class_waitlist=ticket.class_waitlist,
                position=ticket.position - 1
            )
            ticket.position, other_ticket.position = other_ticket.position, ticket.position
            ticket.save()
            other_ticket.save()
    elif direction == "down":
        other_ticket = StudentTicket.objects.filter(
            class_waitlist=ticket.class_waitlist,
            position=ticket.position + 1
        ).first()
        if other_ticket:
            ticket.position, other_ticket.position = other_ticket.position, ticket.position
            ticket.save()
            other_ticket.save()

    return redirect('detail', pk=ticket.class_waitlist.id)
