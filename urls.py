# -*- coding: utf-8 -*-

# pylint: disable=invalid-name
import os

from django.conf.urls import include, url
from django.contrib import admin
from django.shortcuts import redirect
from django.urls.base import reverse


def home(request):
    """ Permit to not get 404 while testing. """
    return redirect(reverse("survey-list"))


urlpatterns = [
    url(r"^$", home, name="home"),
    url(r'^survey/', include('survey.urls')),
    url(r'^admin/', include(admin.site.urls)),
]

if os.getenv("ENVIRONMENT_SETTINGS") != "PRODUCTION":
    urlpatterns.append(url(r'^rosetta/', include('rosetta.urls')))
