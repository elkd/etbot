from django.contrib import admin
from django.contrib.auth.models import User, Group, Site
from autopost.models import EtoroUser, ScheduledPost, UploadReport


admin.site.register(ScheduledPost)
admin.site.register(EtoroUser)
admin.site.register(UploadReport)


admin.site.unregister(User)
admin.site.unregister(Group)
admin.site.unregister(Site)
