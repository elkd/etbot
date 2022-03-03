import itertools
from django.utils.text import slugify

from django.db import models
from django.conf import settings



class EtoroUser(models.Model):
    username = models.CharField(max_length=64)
    password = models.CharField(max_length=64)
    timestamp = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.username


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
    image = models.ImageField(upload_to="images/", null=True, blank=True, max_length=1000)
    timestamp = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(
        max_length=300, null=True,
        blank=True, unique=True, editable=False
    )
    status = models.CharField(max_length=1, choices=STATUS, default=AWAITING)
    post_time = models.DateTimeField(null=True, blank=True)


    class Meta:
        ordering = ("-timestamp",)
        verbose_name = "ScheduledPost"
        verbose_name_plural = "ScheduledPosts"

    def __str__(self):
        return self.content[:50]

    def get_absolute_url(self):
        pass
        #I haven't defined the url yet
        #return reverse('autopost:post_details', args=[self.slug])

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = first_slug = slugify(self.content[:40])

            for x in itertools.count(1):
                if not ScheduledPost.objects.filter(slug=self.slug).exists():
                    break
                self.slug = '%s-%d' % (first_slug, x)
        super().save(*args, **kwargs)


class UploadReport(models.Model):
    post = models.ForeignKey(
            ScheduledPost,
            related_name='reports',
            on_delete=models.CASCADE
        )
    notes = models.TextField(null=True, blank=True)
    exception = models.TextField(null=True, blank=True)
    cookies = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to="uploadreport/", null=True, blank=True, max_length=1000)
    timestamp = models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering = ("-timestamp",)

    def __str__(self):
        return self.notes[:40]
