from pydoc import describe
from urllib.request import Request
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Squad, Topic, Message , User

from django.db.models import Q
# import the model into this file
from django.db.models import Q
from django.contrib import messages  # flash messages
from .forms import SquadForm, UserForm
from django.contrib.auth import authenticate, login, logout
# for restricting users from certain pages  based on if they are logged inor not
from django.contrib.auth.decorators import login_required
# from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm
# Create your views here.


def loginController(request):

    # if a user is logged in do not allow him to go to login page
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(email = email)

            user = authenticate(request, email = email, password=password)

            if user is not None:
                # this registers a session and logs in the user in the browser
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, "Incorrect credentials !!")
        except:
            messages.error(request, "User does not exist !")

    page = "login"
    context = {"page": page}
    return render(request, 'base/signup_login.html', context)


def logoutController(request):
    logout(request)
    return redirect('home')


def registerController(request):
    if request.user.is_authenticated:
        return redirect('home')

    # handling the post request once user hits register button

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # If you call save() with commit=False , then it will return an object that hasn't yet been saved to the database. In this case, it's up to you to call save() on the resulting model instance.
            # this is because we want to do some checks on our own , like username should be all lowe case and stuff
            user.username = user.username.lower()
            user.save()
            # here we completely save it

            # login the user
            login(request, user)

            # redirect him to home page
            return redirect('home')
        else:
            messages.error(request, "An error occured while registration !")

    page = "register"
    form = CustomUserCreationForm()
    context = {"page": page, "form": form}
    return render(request, 'base/signup_login.html', context)


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    squads = Squad.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )

    # get all the topics so that we display them on our home page
    topics = Topic.objects.all()
    squad_count = squads.count()
    # squad_count = 0

    # getting recent activities ,only the 10 most recent
    recent_feed = Message.objects.all().order_by(
        '-created').filter(Q(squad__topic__name__icontains=q))[:10]
    #  we filter the recent feeds as per the topic we are viewing/as per the search

    context = {"squads": squads, "topics": topics,
               "squad_count": squad_count, "recent_feed": recent_feed}
    return render(request, 'base/home.html', context)


def squad(request, pk):
    squad = Squad.objects.get(id=pk)
    messages = squad.message_set.all().order_by('-created')

    # handling the POST requests when someone submits
    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            squad=squad,
            body=request.POST.get('body')
        )
        squad.squadMembers.add(request.user)
        return redirect('squad', pk=squad.id)

    squadMembers = squad.squadMembers.all()

    context = {"squad": squad, "chats": messages, "squadMembers": squadMembers}
    return render(request, 'base/squad.html', context)


# create
# here we use a decorator , if user is not logged in he is not allowed to create a squad , so we redirect him to login page

@login_required(login_url='login')
def createSquad(request):

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)

        squad = Squad.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
        )
        squad.squadMembers.add(request.user)
        squad.save()
        return redirect('home')

    form = SquadForm()
    topics = Topic.objects.all()
    context = {"form": form, "topics": topics}
    return render(request, 'base/squad_form.html', context)

# update


@login_required(login_url='login')
def updateSquad(request, pk):
    squad = Squad.objects.get(id=pk)
    form = SquadForm(instance=squad)  # to prefill the data
    topics = Topic.objects.all()
    context = {'form': form, "topics": topics, "squad": squad}

    if request.user != squad.host:
        return HttpResponse('You are allowed for this action !')

    # to save the data to db
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)

        squad.name = request.POST.get('name')
        squad.description = request.POST.get('description')
        squad.topic = topic
        squad.save()

        return redirect('home')

    return render(request, 'base/squad_form.html', context)

# delete


@login_required(login_url='login')
def deleteSquad(request, pk):
    squad = Squad.objects.get(id=pk)

    if request.user != squad.host:
        return HttpResponse('You are allowed for this action !')

    if(request.method == 'POST'):
        squad.delete()
        return redirect('home')
    context = {'obj': squad}
    return render(request, 'base/delete.html', context)


def deleteChat(request, pk):
    message = Message.objects.get(id=pk)
    if request.method == 'POST':
        message.delete()
        return redirect('home')

    return render(request, 'base/delete.html', {'obj': message})


def profile(request, pk):
    user = User.objects.get(id=pk)
    squads = user.squad_set.all()
    recent_feed = user.message_set.all()[:10]
    context = {"user": user, "squads": squads, "recent_feed": recent_feed}
    return render(request, 'base/profile.html', context)


@login_required(login_url="home")
def updateProfile(request):
    user = request.user
    form = UserForm(instance=user)
    context = {"form": form}

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES , instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile', pk=user.id)

    return render(request, 'base/update-profile.html', context)
