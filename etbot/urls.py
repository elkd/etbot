"""etbot URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.views.generic import RedirectView, TemplateView
from django.conf.urls.static import static

from autopost.views import PostListView, CreatePostView, HomepageView, PostDetailView


admin.site.site_header = "BabylonBot Dashboard"
admin.site.site_title = "BabylonBot Admin Dashboard"
admin.site.index_title = "Welcome to BabylonBot Admin Dashboard"


urlpatterns = [
    path('', HomepageView.as_view(), name='home'),
    path(settings.ADMIN_URL, admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),

    path('posting-schedule/', PostListView.as_view(), name='posts_list'),
    path('posting-schedule/new/', CreatePostView.as_view(), name='new_post'),
    path('posting-schedule/<int:pk>', PostDetailView.as_view(), name='post_detail'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
