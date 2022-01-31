from django.shortcuts import render
from django.views import generic
from autopost.models import ScheduledPosts

from bootstrap_datepicker_plus.widgets import DateTimePickerInput


class CreatePostView(generic.edit.CreateView):
    model=ScheduledPosts
    template_name = 'autopost/new_post.html'
    #success_url = reverse_lazy('app:index')
    fields = ['content', 'image','author', 'post_time']

    def get_form(self):
        form = super().get_form()
        form.fields['post_time'].widget = DateTimePickerInput()
        return form


def post_list_view(request):
    pass
