"""
    For student activity: enroll, learn, quiz, ...
"""
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from module_group.models import ModuleGroup

from ..models import Course, Quiz, Question, Answer_Option

from django.contrib.auth.decorators import login_required, user_passes_test


@login_required
def short_link_course(request, course_pk):
    course = get_object_or_404(Course, pk=course_pk)
    course_name = course.url()
    return redirect(reverse('course:course', kwargs={'course_pk': course_pk, 'course_name': course_name}))


@login_required
def course(request, course_pk, course_name):
    course = get_object_or_404(Course, pk=course_pk)
    if course_name != course.url():
        raise Http404("Incorrect course name!")