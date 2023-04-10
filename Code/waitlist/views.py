from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect

def waitlistHome(request):
    return redirect('/studenthome/')
