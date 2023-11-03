from django.contrib import admin
from .models import Task, Comment,Parts,Clients,Personal,Notification
admin.site.register(Task)
admin.site.register(Comment)
admin.site.register(Parts)
admin.site.register(Clients)
admin.site.register(Personal)
admin.site.register(Notification)

