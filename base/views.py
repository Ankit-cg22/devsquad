from django.shortcuts import render , redirect
from .models import Squad
#import the model into this file

from .forms import SquadForm

#Create your views here.

def home(request):
    squads = Squad.objects.all()
    context = {"content" : squads}
    return render(request , 'base/home.html' , context)

def squad(req , pk):
    squad = Squad.objects.get(id = pk)
    context = {"squad" : squad}
    return render(req , 'base/squad.html' , context)

def createSquad(request):
    if request.method == 'POST':
        form = SquadForm(request.POST)
        if( form.is_valid()) :
            form.save()
            return redirect('home')
    form = SquadForm()
    context = {"form" : form }
    return render(request , 'base/squad_form.html' , context)

def updateSquad(request , pk):
    squad = Squad.objects.get(id=pk)
    form = SquadForm(instance = squad) #to prefill the data
    context = {'form' : form}

    # to save the data to db 
    if request.method == 'POST':
        form = SquadForm(request.POST , instance = squad)
        if form.is_valid :
            form.save()
            return redirect('home')
    return render(request , 'base/squad_form.html' , context)

def deleteSquad(request , pk):
    room = Squad.objects.get(id = pk)
    if(request.method == 'POST'):
        room.delete()
        return redirect('home')
    context = {'obj' : room}
    return render(request , 'base/delete.html' , context)