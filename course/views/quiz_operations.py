from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.db.utils import IntegrityError

from module_group.models import ModuleGroup

from ..models import *

from django.contrib.auth.decorators import login_required
from main.utils.block import custom_user_passes_test, block_unenrolled_student

from .utils import query_all_sub_courses


@login_required
@custom_user_passes_test(block_unenrolled_student, "course:short_link_course", ["course_pk"])
def short_link_quiz(request, course_pk, quiz_pk):
    course = get_object_or_404(Course, pk=course_pk)
    course_name = course.url()
    
    quiz = get_object_or_404(Quiz, pk=quiz_pk)

    return redirect(reverse('course:quiz_preview', kwargs={'course_pk': course_pk, 'course_name': course_name, 'quiz_pk': quiz_pk}))


@login_required
@custom_user_passes_test(block_unenrolled_student, "course:short_link_course", ["course_pk"])
def quiz_preview(request, course_pk, course_name, quiz_pk):
    course = get_object_or_404(Course, pk=course_pk)
    if course_name != course.url():
        raise Http404("Incorrect course name!")
    
    course = get_object_or_404(Course, pk=course_pk)
    course_name = course.url()
    
    quiz = get_object_or_404(Quiz, pk=quiz_pk)
    sub_course_pk = quiz.sub_course.id
    num_of_questions = len(quiz.questions.all())

    context = {
        "course" : course,
        "sub_course_pk" : sub_course_pk,
        "num_of_questions" : num_of_questions,
        "quiz": quiz,
        "sub_courses" : {},
    }
    query_all_sub_courses(course, context)

    return render(request, 'course_operations/main_view.html', context)