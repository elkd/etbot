from django.contrib import admin
from autopost.models import EtoroUser, ScheduledPost

admin.site.register(ScheduledPost)
admin.site.register(EtoroUser)
