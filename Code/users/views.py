from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm
from django.contrib.auth.models import Group
# Create your views here.
def register(request):
    if request.method =='POST':
        form =UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save() #automatically hashes password and saves user
            if (form.cleaned_data.get('isProfessor')):
                group = Group.objects.get(name='Professor')
                user.groups.add(group)
            else:
                group = Group.objects.get(name='Student')
                user.groups.add(group)
            user.save()
            first = form.cleaned_data.get('first_name')
            last = form.cleaned_data.get('last_name')
            messages.success(request,f'Account created for {first} {last}')
            return redirect('login')
    else:
        form =UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


def profile(request):
    return render(request, 'users/profile.html')
