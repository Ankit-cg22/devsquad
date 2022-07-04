'''
in this file we create the forms that we need 

'''

from dataclasses import fields
from django.forms import ModelForm
from .models import Squad
from django.contrib.auth.models import User


class SquadForm(ModelForm):
    class Meta:
        model = Squad
        fields = '__all__'
        # this create a model form for us which contains all the fields of the Squad model
        exclude = ["host", "squadMembers"]
        # we do want to include these two fields in the form
        # we will automatically set the host as the user who is logged in
        # and for squadMemebers , they get added automatically when they interact with the squad


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']
        exclude = []
