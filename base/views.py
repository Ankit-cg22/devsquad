from pydoc import describe
from urllib.request import Request
from django.http import HttpResponse
from django.shortcuts import render , redirect
from .models import Squad , Topic 
from django.contrib.auth.models import User
from django.db.models import Q
#import the model into this file
from django.db.models import Q
from django.contrib import messages #flash messages
from .forms import SquadForm 
from django.contrib.auth import authenticate , login , logout
# for restricting users from certain pages  based on if they are logged inor not
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
#Create your views here.

def loginController(request):

    # if a user is logged in do not allow him to go to login page 
    if request.user.is_authenticated :
        return redirect('home')

    if request.method ==  'POST' : 
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username = username)

            user = authenticate(request , username = username , password = password )

            if user is not None :
                login(request , user) # this registers a session and logs in the user in the browser
                return redirect('home')
            else :
                messages.error(request , "Incorrect credentials !!")
        except :
            messages.error(request , "User does not exist !")

        
    page ="login"
    context = {"page" : page}
    return render(request , 'base/signup_login.html' , context)

def logoutController(request):
    logout(request)
    return redirect('home')

def registerController(request):
    if request.user.is_authenticated :
        return redirect('home')

    # handling the post request once user hits register button 

    if request.method == 'POST' : 
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit = False)
            # If you call save() with commit=False , then it will return an object that hasn't yet been saved to the database. In this case, it's up to you to call save() on the resulting model instance.
            # this is because we want to do some checks on our own , like username should be all lowe case and stuff
            user.username = user.username.lower()
            user.save()
            # here we completely save it 
            
            # login the user
            login(request , user)

            # redirect him to home page
            return redirect('home')
        else :
            messages.error(request , "An error occured while registration !")

    page = "register"
    form = UserCreationForm()
    context = {"page" : page , "form" : form }
    return render(request , 'base/signup_login.html' , context )


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    

    '''
    squads = Squad.objects.filter(topic__name__contains = q)
    # __contains means if q is a substring of topic name it is accepted in the filter
    # if no query is made , then q = "" 
    # "" is a substring of every word , so all squads are returned

    # here we are only searching matching topic names 
    # but we also want to include matching squad title , squad desctiptions etc
    '''

    squads = Squad.objects.filter(
        Q(topic__name__icontains = q) | 
        Q(name__icontains = q) |
        Q(description__icontains = q)
        )

    #get all the topics so that we display them on our home page
    topics = Topic.objects.all()
    squad_count = squads.count()

    context = {"squads" : squads , "topics" : topics , "squad_count" : squad_count}
    return render(request , 'base/home.html' , context)

def squad(req , pk):
    squad = Squad.objects.get(id = pk)
    context = {"squad" : squad}
    return render(req , 'base/squad.html' , context)

# create
# here we use a decorator , if user is not logged in he is not allowed to create a squad , so we redirect him to login page 
@login_required(login_url = 'login')
def createSquad(request):
    if request.method == 'POST':
        form = SquadForm(request.POST)
        if( form.is_valid()) :
            form.save()
            return redirect('home')
    form = SquadForm()
    context = {"form" : form }
    return render(request , 'base/squad_form.html' , context)

# update
@login_required(login_url = 'login')
def updateSquad(request , pk):
    squad = Squad.objects.get(id=pk)
    form = SquadForm(instance = squad) #to prefill the data
    context = {'form' : form}

    if request.user != squad.host :
        return HttpResponse('You are allowed for this action !')

    # to save the data to db 
    if request.method == 'POST':
        form = SquadForm(request.POST , instance = squad)
        if form.is_valid :
            form.save()
            return redirect('home')

    return render(request , 'base/squad_form.html' , context)

# delete
@login_required(login_url = 'login')
def deleteSquad(request , pk):
    squad = Squad.objects.get(id = pk)

    if request.user != squad.host :
        return HttpResponse('You are allowed for this action !')

    if(request.method == 'POST'):
        squad.delete()
        return redirect('home')
    context = {'obj' : squad}
    return render(request , 'base/delete.html' , context)