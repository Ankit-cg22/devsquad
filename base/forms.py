'''
in this file we create the forms that we need 

'''

from dataclasses import fields
from django.forms import ModelForm
from .models import Squad

class SquadForm(ModelForm):
    class Meta :
        model = Squad
        fields = '__all__'
    # this create a model form for us which contains all the fields of the Squad model 