from django.conf.urls import url
from survey_admin.views import (
    IndexView, DashboardView, CombinedResponses)


urlpatterns = [
    url(r'^$', IndexView.as_view()),
    url(r'^dashboard/$', DashboardView.as_view()),
    url(r'^combined-responses/(?P<pk>\d+)/',
        CombinedResponses.as_view())
]
