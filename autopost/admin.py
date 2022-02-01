from django.contrib import admin
from autopost.models import EtoroUser, ScheduledPost, UploadReport

admin.site.register(ScheduledPost)
admin.site.register(EtoroUser)
admin.site.register(UploadReport)
