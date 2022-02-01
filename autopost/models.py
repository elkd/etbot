from django.db import models
from django.conf import settings


class EtoroUser(models.Model):
    username = models.CharField(max_length=64)
    password = models.CharField(max_length=64)
    timestamp = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(null=True, blank=True)


class ScheduledPost(models.Model):
    FAILED = "F"
    AWAITING = "A"
    POSTED = "P"
    STATUS = (
        (FAILED, "Failed"),
        (AWAITING, "Pending"),
        (POSTED, "Posted")
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True,
        related_name="creater", on_delete=models.CASCADE
    )
    author = models.ForeignKey(
        EtoroUser, related_name="etoro_user",
        on_delete=models.CASCADE, null=True, blank=True
    )
    content = models.TextField()
    image = models.ImageField(upload_to="images/", null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(
        max_length=300, null=True,
        blank=True, unique=True, editable=False
    )
    status = models.CharField(max_length=1, choices=STATUS, default=AWAITING)
    post_time = models.DateTimeField(null=True, blank=True)


class UploadReport(models.Model):
    post = models.ForeignKey(
            ScheduledPost,
            related_name='reports',
            on_delete=models.CASCADE
        )
    notes = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
