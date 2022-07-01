from django.db import models

# importing the User model which is in built by django
from django.contrib.auth.models import User 

# Create your models here.

# Topic model : each squad will belong to a particular topic
class Topic(models.Model) :
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

# model to store the squads 
class Squad(models.Model):
    host  = models.ForeignKey(User , on_delete = models.SET_NULL , null=True)
    # one to one , each squad can have one host

    topic  = models.ForeignKey(Topic , on_delete=models.SET_NULL , null=True)
    # one to many , each squad can have one topic(for now)

    name = models.CharField(max_length=200)
    description = models.TextField(null = True , blank = True) 
    squadMembers = models.ManyToManyField(User , related_name = "squadMembers" , blank = True) 
    updated = models.DateTimeField(auto_now = True)
    # auto_now takes a timestamp every time the model is updated 
    created = models.DateTimeField(auto_now_add = True)
    # auto_now_add takes a timestamp only when we add it the first time 

    class Meta:
        ordering = ['-updated' , '-created']

    def __str__(self):
        return self.name


# Message model : to store the messages / chats sent by a user 
class Message(models.Model):
    
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    # one to many : user can have many messages 

    squad = models.ForeignKey(Squad , on_delete = models.CASCADE) 
    # this is a many to one relation , one squad can be related with many messages 
    # it means when the parent(squad) is delete , cascade(delete) these messages

    body = models.TextField()
    updated = models.DateTimeField(auto_now  = True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body[0:50]
        # here we take the first 50 characters of the message