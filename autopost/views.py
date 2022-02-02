from django.shortcuts import render
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from bootstrap_datepicker_plus.widgets import DateTimePickerInput

from autopost.models import ScheduledPost, EtoroUser
from autopost.tasks import post_task


class CreatePostView(CreateView, LoginRequiredMixin):
    model=ScheduledPost
    template_name = 'autopost/new_post.html'
    success_url = reverse_lazy('new_post')
    success_message = "Successfully Created a new post, To be uploaded later!"
    fields = ['content', 'image','author', 'post_time']

    def get_form(self):
        form = super().get_form()
        form.fields['post_time'].widget = DateTimePickerInput()
        return form

    def form_valid(self, form):
        form.instance.user = self.request.user
        self.object = form.save()

        post_task.apply_async(
            kwargs={"pid":self.object.id},
            eta=self.object.post_time,
        )
        return HttpResponseRedirect(self.get_success_url())


def post_list_view(request):
    pass
