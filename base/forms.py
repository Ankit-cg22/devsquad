'''
in this file we create the forms that we need 

'''

from dataclasses import fields
from django.forms import ModelForm
from .models import Squad ,User
from django.contrib.auth.forms import UserCreationForm

class SquadForm(ModelForm):
    class Meta:
        model = Squad
        fields = '__all__'
        # this create a model form for us which contains all the fields of the Squad model
        exclude = ["host", "squadMembers"]
        # we do want to include these two fields in the form
        # we will automatically set the host as the user who is logged in
        # and for squadMemebers , they get added automatically when they interact with the squad

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name' , 'username' , 'email' , 'password1' , 'password2']

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = [ 'profilePicture', 'name' ,'username', 'email' ,'bio' ]
        exclude = []
