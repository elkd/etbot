from django.conf import settings
import pytest
from autopost.tasks import post_task
from autopost.models import ScheduledPost, EtoroUser, UploadReport
from settings import env


MEDIA_PATH=env('MEDIA_PATH')


def test_success():
    etuser = EtoroUser.objects.create(
        username='BAbylonFund',
        password='Babylon33!'
    )
    post = ScheduledPost.objects.create(
        author = etuser,
        content = 'Dear Copier',
        image = '/'.join([MEDIA_PATH, 'images/copiers-post_tXkaMnD.png'])
    )
    post_task(post.id)
    assert UploadReport.objects.latest('timestamp').notes == 'Successfully Uploaded the post On Etoro Website'
    #product_order.assert_called_with(3, Decimal(30.3))
