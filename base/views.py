from django.shortcuts import render
from .models import Squad
#import the model into this file

#Create your views here.

def home(request):
    squads = Squad.objects.all()
    context = {"content" : squads}
    return render(request , 'base/home.html' , context)

def squad(req , pk):
    room = Squad.objects.get(id = pk)
    context = {"room" : room}
    return render(req , 'base/squad.html' , context)