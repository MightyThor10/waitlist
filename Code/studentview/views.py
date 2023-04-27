from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views import generic
from .models import ClassWaitlist, StudentTicket
from django.contrib.auth.models import User, Group
from django.utils import timezone
from django.contrib import messages
from django import forms
from django.db.models import Q

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
        message = ''

        if not classid:
            message = 'You must enter a class id'
        else:
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
        
        searchTerm = request.GET.get('searchTerm', '')

        classes = ClassWaitlist.objects.filter(Q(className__contains=searchTerm) | Q(crn__contains=searchTerm)| Q(classCode__contains=searchTerm) | Q(professor__username__contains=searchTerm))

        context = {
            'title': 'join waitlist',
            'classes': classes,
            'searchTerm' : searchTerm
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

def leave_all_waitlists(request):
    user = request.user
    message = ""

    if user:
        existing_tickets = StudentTicket.objects.filter(student=user)
        existing_tickets.delete()
        message = "You have successfully left all waitlists."
        response = redirect('/studenthome/')
        return response
    else:
        message = "Invalid user."

    context = {
        'title': 'leave all waitlists',
        'message': message,
        'classes': ClassWaitlist.objects.all(),
    }
    return render(request, 'studentview/leave_all_waitlists.html', context)

def createWaitlist(request):

    if request.method =='POST':
        name = request.POST['className']
        desc = request.POST['classDesc']
        code = request.POST['classCode']
        crn = request.POST['classCRN']
        crn2 = request.POST['classCRN2']
        crn3 = request.POST['classCRN3']

        schedule = request.POST['firstSectionSchedule']
        schedule2 = request.POST['secondSectionSchedule']
        schedule3 = request.POST['thirdSectionSchedule']
        sortType = request.POST['classSort']
        term = request.POST['classTerm']
        datePosted = timezone.now()
        user = request.user
        anonymous_waitlist = request.POST.get('anonymous_waitlist', 'False') == 'on'
        # StudentTicket.objects.create(class_waitlist=waitlist, date_joined= timezone.now(), student=user)
        
        cwl = ClassWaitlist.objects.create(className=name+" Section 1", classDescription=desc, classCode=code, crn=crn, schedule=schedule, sortType=sortType, term=term, date_added=datePosted, professor=user, anonymous_waitlist=anonymous_waitlist)
        if schedule2 != "" or crn2 != "":
            cw2 = ClassWaitlist.objects.create(className=name+" Section 2", classDescription=desc, classCode=code, crn=crn2, schedule=schedule2, sortType=sortType, term=term, date_added=datePosted, professor=user, anonymous_waitlist=anonymous_waitlist)
        if schedule3 != "" or crn3 != "":
            cw3 = ClassWaitlist.objects.create(className=name+" Section 3", classDescription=desc, classCode=code, crn=crn3, schedule=schedule3, sortType=sortType, term=term, date_added=datePosted, professor=user, anonymous_waitlist=anonymous_waitlist)


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
        print(kwargs)
        context = super().get_context_data(**kwargs)
        context['isProfessor'] = self.request.user.groups.filter(name='Professor').exists()
        context['ownsClass'] = self.request.user.id == kwargs['object'].professor.pk
        context['anonymous_waitlist'] = kwargs['object'].anonymous_waitlist
        return context
    

class EditWaitlistForm(forms.ModelForm):
    class Meta:
        model = ClassWaitlist
        fields = ['className', 'classDescription', 'classCode', 'crn', 'schedule', 'sortType', 'term', 'anonymous_waitlist']


class EditView(LoginRequiredMixin, generic.UpdateView):

    model = ClassWaitlist
    form_class = EditWaitlistForm
    template_name = 'studentview/edit_waitlist.html'

    def get(self, request, *args, **kwargs):
        userid = request.user.id
        classProfessorId = ClassWaitlist.objects.filter(pk=kwargs['pk']).first().professor.pk #there is for sure a better way to do this lol, but this works
        print(classProfessorId)
        if userid == classProfessorId:
            return super().get(request, *args, **kwargs)
        return render({}, '403') # goes to 404 but making idk how to make it go to a 403 page instead
        

    def get_success_url(self):
        print(self.model.id)
        return "../detail"

    

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
def update_waitlist_status(request, ticket_id, newstatus):
    ticket = get_object_or_404(StudentTicket, id=ticket_id)
    ticket.waitlist_status=newstatus
    ticket.save()
    return redirect('detail', pk=ticket.class_waitlist.id)