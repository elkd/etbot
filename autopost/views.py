from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from bootstrap_datepicker_plus.widgets import DateTimePickerInput

from autopost.models import ScheduledPost, EtoroUser
from autopost.post import post_now


class CreatePostView(CreateView, LoginRequiredMixin):
    model=ScheduledPost
    template_name = 'autopost/new_post.html'
    #success_url = reverse_lazy('app:index')
    fields = ['content', 'image','author', 'post_time']

    def get_form(self):
        form = super().get_form()
        form.fields['post_time'].widget = DateTimePickerInput()
        return form

    def form_valid(self, form):
        form.instance.user = self.request.user
        self.object = form.save()

        etuser = EtoroUser.objects.get(id=self.object.author.id)
        post_now(etuser.username, etuser.password, self.object.content, self.object.image)
        return HttpResponseRedirect(self.get_success_url())


def post_list_view(request):
    pass
