import pytest
from etbot.settings import env
from autopost.tasks import post_task, login, start_browser
from autopost.models import ScheduledPost, EtoroUser, UploadReport


MEDIA_PATH=env('MEDIA_PATH')

pytestmark = pytest.mark.django_db

@pytest.fixture
def etoro_user():
    return EtoroUser.objects.create(
        username=env('ETOROUSER'),
        password=env('ETOROPASSWORD')
    )


@pytest.fixture
def scheduled_post(etoro_user):
    return ScheduledPost.objects.create(
        author = etoro_user,
        content = 'Dear Copier',
        image = '/'.join([MEDIA_PATH, 'images/copiers-post_tXkaMnD.png'])
    )


@pytest.fixture(scope='session')
def browser():
    browser = start_browser(mode='human', profile=False)
    yield browser
    browser.close()


def defertest_login(etoro_user, scheduled_post, browser):
    res, title = login( browser,
        username=etoro_user.username,
        password=etoro_user.password,
        post=scheduled_post,
        timeout=20
    )

    if str(browser.current_url).endswith('home') or browser.title == "eToro":
        res = browser.title

    assert res is not None


def defertest_post(etoro_user, scheduled_post):
    ''' This test needs mocking in a sense that the upload function should not finish
    The upload function can be returning when the upload form is opened'''

    assert UploadReport.objects.latest('timestamp').notes == 'Successfully Uploaded the post On Etoro Website'

    #If we passed schedule_post as function argument we can assert
    scheduled_post.assert_called_with(post.id)
