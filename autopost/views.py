from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from django.views.generic import (
        CreateView, UpdateView, ListView,
        DetailView, DeleteView, TemplateView
    )
from bootstrap_datepicker_plus.widgets import DateTimePickerInput

from autopost.models import ScheduledPost, EtoroUser, UploadReport
from autopost.tasks import post_task


class HomepageView(TemplateView):
    template_name = 'home.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('posts_list')
        else:
            context = self.get_context_data(**kwargs)
            return self.render_to_response(context)



class PostListView(LoginRequiredMixin, ListView):
    model=ScheduledPost
    context_object_name = 'data'
    template_name = 'autopost/posts_list.html'

    def get_queryset(self):
        all_posts = ScheduledPost.objects.all().order_by('-timestamp')

        pending = all_posts.filter(
                    status='A'
                )

        posted = all_posts.filter(
                    status='P'
                )
        reports = UploadReport.objects.all()[:5]

        return {'all_posts': all_posts, 'pending': pending, 'posted': posted, 'reports':reports}


class PostDetailView(LoginRequiredMixin, DetailView):
    model=ScheduledPost
    context_object_name = 'post'


class CreatePostView(LoginRequiredMixin, CreateView):
    model=ScheduledPost
    template_name = 'autopost/new_post.html'
    success_message = "Successfully Created a new pending post"
    fields = ['content', 'image','author', 'post_time']

    def get_form(self):
        form = super().get_form()
        form.fields['post_time'].widget = DateTimePickerInput()
        return form

    def form_valid(self, form):
        form.instance.user = self.request.user
        self.object = form.save()

        post_task.apply_async(
            kwargs={"postid":self.object.id},
            eta=self.object.post_time,
        )
        return redirect('posts_list')
