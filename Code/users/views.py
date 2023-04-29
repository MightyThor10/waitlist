from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from .forms import UserRegisterForm, StudentProfileForm, CustomPasswordChangeForm
from django.contrib.auth.models import Group
from .models import StudentProfile
from django.core.mail import send_mail

def send_welcome_email(user, group_name):
    subject = 'Welcome to the Waitlist Management System'
    if group_name == 'Professor':
        message = f'Dear Professor {user.first_name} {user.last_name},\n\nCongratulations on joining the Waitlist Management System! You can now access the platform to manage your course waitlists.\n\nBest regards,\nThe Waitlist Management System Team'
    else:
        message = f'Dear {user.first_name} {user.last_name},\n\nCongratulations on joining the Waitlist Management System! You can now access the platform to join course waitlists.\n\nBest regards,\nThe Waitlist Management System Team'
    from_email = 'waitlistprojectwm@gmail.com'
    recipient_list = [user.email]
    send_mail(subject, message, from_email, recipient_list)


# Create your views here.
def register(request):
    if request.method =='POST':
        form =UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save() #automatically hashes password and saves user
            if (request.POST.get('isProfessor', False)):
                group = Group.objects.get(name='Professor')
                user.groups.add(group)
            else:
                group = Group.objects.get(name='Student')
                user.groups.add(group)
            user.save()
            send_welcome_email(user, group.name) # Send welcome email
            first = form.cleaned_data.get('first_name')
            last = form.cleaned_data.get('last_name')
            messages.success(request,f'Account created for {first} {last}')
            return redirect('login')
    else:
        form =UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


def change_passwordNotification(user):
    subject = 'IMPORTANT: Your password has been changed'
    message = f'Dear {user.first_name} {user.last_name},\n\n We are sending you this email to confirm that your password for the Waitlist Management System has been successfully changed. If you did not initiate this change, please contact our support team immediately at waitlistprojectwm@gmail.com. \n\nBest regards,\nThe Waitlist Management System Team'
    from_email = 'waitlistprojectwm@gmail.com'
    recipient_list = [user.email]
    send_mail(subject, message, from_email, recipient_list)

@login_required
def profile(request):
    # Create studentprofile if it does not exist
    StudentProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        if 'update_profile' in request.POST:
            profile_form = StudentProfileForm(request.POST, instance=request.user.studentprofile)
            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, 'Your profile has been updated!')
                return redirect('profile')
        elif 'change_password' in request.POST:
            password_form = CustomPasswordChangeForm(request.user, request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                change_passwordNotification(user)
                messages.success(request, 'Your password has been changed!')
                return redirect('profile')

    # Populate the initial value of academic status based on the student's current academic status
    student_profile = request.user.studentprofile
    initial = {
        'academic_status': student_profile.academic_status if student_profile.academic_status else None,
    }

    profile_form = StudentProfileForm(instance=student_profile, initial=initial)
    password_form = CustomPasswordChangeForm(request.user)

    return render(request, 'users/profile.html', {'profile_form': profile_form, 'password_form': password_form})


