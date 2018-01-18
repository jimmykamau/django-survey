# -*- coding: utf-8 -*-

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

from builtins import open

from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, render
from future import standard_library
from survey.exporter.csv.survey2csv import Survey2Csv
from survey.models import Category, Survey, Question, Answer

standard_library.install_aliases()


def serve_unprotected_result_csv(survey):
    """ Return the csv corresponding to a survey. """
    s2csv = Survey2Csv(survey)
    if s2csv.need_update():
        s2csv.generate_file()
    with open(s2csv.file_name(), 'r') as csv_file:
        response = HttpResponse(csv_file.read(), content_type='text/csv')
    content_disposition = u'attachment; filename="{}.csv"'.format(survey.name)
    response['Content-Disposition'] = content_disposition
    return response


@login_required
def serve_protected_result(request, survey):
    """ Return the csv only if the user is logged. """
    return serve_unprotected_result_csv(survey)


def serve_result_csv(request, pk):
    """ ... only if the survey does not require login or the user is logged.

    :param int pk: The primary key of the survey. """
    survey = get_object_or_404(Survey, pk=pk)
    if survey.need_logged_user:
        return serve_protected_result(request, survey)
    else:
        return serve_unprotected_result_csv(survey)


@staff_member_required
def serve_result_single_page(request, pk):
    template_name = 'survey/combined_results.html'
    survey = get_object_or_404(Survey, pk=pk)
    categories = Category.objects.filter(survey=survey).order_by('order')
    questions = Question.objects.filter(survey=survey).order_by('order')
    answers = Answer.objects.all()
    context = {
        'survey': survey,
        'categories': categories,
        'questions': questions,
        'answers': answers
    }
    return render(request, template_name, context)
