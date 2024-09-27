"""
    For student activity: enroll, learn, quiz, ...
"""
import ast
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.db.utils import IntegrityError

from module_group.models import ModuleGroup

from ..models import Course, Quiz, Question, Answer_Option, Enrolled_course, Module, Sub_Course, Sub_Module

from django.contrib.auth.decorators import login_required, user_passes_test


@login_required
def short_link_course(request, course_pk):
    course = get_object_or_404(Course, pk=course_pk)
    course_name = course.url()
    return redirect(reverse('course:course_preview', kwargs={'course_pk': course_pk, 'course_name': course_name}))


@login_required
def course_preview(request, course_pk, course_name):
    course = get_object_or_404(Course, pk=course_pk)
    if course_name != course.url():
        raise Http404("Incorrect course name!")

    created_by = set()

    enrolled_user = course.enrolled_user.filter(user= request.user)
    is_enrolled = True if enrolled_user else False

    context = {
        "course" : course,
        "created_by" : created_by,
        "is_enrolled" : is_enrolled,
        "sub_courses" : {}
    }

    sub_courses = course.sub_courses.all()
    for sub_course in sub_courses:
        modules = sub_course.modules.all().order_by("order")
        quizzes = sub_course.quizzes.all().order_by("order")
        
        context['sub_courses'][sub_course] = {
            'modules': {},
            'quizzes': quizzes,
        }

        for module in modules:
            sub_modules = module.sub_modules.all().order_by("order")
            created_by.add(module.created_by.full_name)

            context['sub_courses'][sub_course]['modules'][module] = sub_modules

    return render(request, 'course_operations/course_preview.html', context)
    

@login_required
def course_enroll(request, course_pk):
    course = get_object_or_404(Course, pk=course_pk)
    
    try:
        enrolling = Enrolled_course(course= course, user=request.user)
        enrolling.save()
    except IntegrityError:
        pass

    return redirect(reverse('course:short_link_course', kwargs={'course_pk': course_pk}))


@login_required
def short_link_sub_course(request, course_pk, sub_module_pk):
    course = get_object_or_404(Course, pk=course_pk)
    course_name = course.url()
    
    sub_module = get_object_or_404(Sub_Module, pk=sub_module_pk)

    return redirect(reverse('course:sub_course_learn', kwargs={'course_pk': course_pk, 'course_name': course_name, 'sub_module_pk': sub_module_pk}))

@login_required
def sub_course_learn(request, course_pk, course_name, sub_module_pk):
    course = get_object_or_404(Course, pk=course_pk)
    if course_name != course.url():
        raise Http404("Incorrect course name!")
    
    sub_module = get_object_or_404(Sub_Module, pk=sub_module_pk)
    module_pk = sub_module.module.id

    content_html_list = ast.literal_eval(sub_module.content_html_list)
    image_list = ast.literal_eval(sub_module.image_list)
    video_url = sub_module.video_url
    title = sub_module.title

    context = {
        "course" : course,
        "title": title,
        "module_pk" : module_pk,
        "sub_module_pk" : sub_module_pk,
        'content_html_list': content_html_list,
        'image_list': image_list,
        'video_url': video_url,
        "sub_courses" : {}
    }

    sub_courses = course.sub_courses.all()
    for sub_course in sub_courses:
        modules = sub_course.modules.all().order_by("order")
        quizzes = sub_course.quizzes.all().order_by("order")
        
        context['sub_courses'][sub_course] = {
            'modules': {},
            'quizzes': quizzes,
        }

        for module in modules:
            sub_modules = module.sub_modules.all().order_by("order")

            context['sub_courses'][sub_course]['modules'][module] = sub_modules

    return render(request, 'course_operations/sub_course_learn.html', context)