from django.contrib import admin

# Register your models here.

from .models import Squad , Topic, Message , User

admin.site.register(Squad)
admin.site.register(Topic)
admin.site.register(Message)
admin.site.register(User)