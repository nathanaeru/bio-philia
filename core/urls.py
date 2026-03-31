"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.shortcuts import render
from django.urls import path, include
from django.views.generic import RedirectView
from biodata.views import edit_theme
from core.views import github_webhook, home_view
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from biodata.views import change_username


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/login/', RedirectView.as_view(url='/accounts/google/login/')),
    path('accounts/signup/', RedirectView.as_view(url='/accounts/google/login/')),
    path('accounts/password/reset/', RedirectView.as_view(url='/')),
    path('accounts/', include('allauth.urls')),
    path('', home_view, name='home_view'),
    path('edit-theme/', edit_theme, name='edit_theme'),
    path('webhook/deploy/', github_webhook, name='github_webhook'),
    path('change-username/', change_username, name='change_username'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
