from django.shortcuts import get_object_or_404, render
from django.views.generic import TemplateView

from survey.models import (
    Answer, Category, Question, Survey)


class IndexView(TemplateView):
    """Handles the index URL, which is the authentication page"""

    def get(self, request):
        return render(request, "index.html")


class DashboardView(TemplateView):
    """docstring for DashboardView"""

    def get(self, request):
        surveys = Survey.objects.order_by('-id')
        context = {
            'surveys': surveys
        }
        return render(request, "dashboard.html", context)


class CombinedResponses(TemplateView):
    """docstring for CombinedResponses"""

    def get(self, request, pk):
        survey = get_object_or_404(Survey, pk=pk)
        categories = Category.objects.filter(survey=survey).order_by('order')
        context = {
            'survey': survey,
            'categories': categories
        }
        return render(request, 'combined_responses.html', context)
