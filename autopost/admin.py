from django.contrib import admin
from autopost.models import EtoroUser, ScheduledPosts

admin.site.register(ScheduledPosts)
admin.site.register(EtoroUser)
