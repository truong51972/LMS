"""
    For student activity: enroll, learn, quiz, ...
"""
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.db.utils import IntegrityError

from module_group.models import ModuleGroup

from ..models import Course, Quiz, Question, Answer_Option, Enrolled_course

from django.contrib.auth.decorators import login_required, user_passes_test


@login_required
def short_link_course(request, course_pk):
    course = get_object_or_404(Course, pk=course_pk)
    course_name = course.url()
    return redirect(reverse('course:course_detail', kwargs={'course_pk': course_pk, 'course_name': course_name}))


@login_required
def course_detail(request, course_pk, course_name):
    course = get_object_or_404(Course, pk=course_pk)
    if course_name != course.url():
        raise Http404("Incorrect course name!")
    quizzes = Quiz.objects.filter(course=course)

    created_by = set()
    for quiz in quizzes:
        created_by.add(quiz.created_by.full_name)

    enrolled_user = course.enrolled_user.filter(user= request.user)
    is_enrolled = True if enrolled_user else False

    print(is_enrolled)
    context = {
        "course" : course,
        "created_by" : created_by,
        "is_enrolled" : is_enrolled,
    }
    return render(request, 'course_operations/course_view.html', context)
    

@login_required
def course_enroll(request, course_pk):
    course = get_object_or_404(Course, pk=course_pk)
    
    try:
        enrolling = Enrolled_course(course= course, user=request.user)
        enrolling.save()
    except IntegrityError:
        pass

    return redirect(reverse('course:short_link_course', kwargs={'course_pk': course_pk}))