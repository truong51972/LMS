import os
import cv2

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from module_group.models import ModuleGroup

from .forms import CourseForm
from .models import Course

from quiz.forms import Quiz_Form
from quiz.models import Quiz

from django.contrib.auth.decorators import login_required
from main.utils.block import block_student
from django.contrib.auth.decorators import user_passes_test

from django.core.cache import cache


def compress_image(image_path):
    img = cv2.imread(image_path)
    img = cv2.resize(img, (400, 225), interpolation=cv2.INTER_AREA)
    cv2.imwrite(image_path, img)


@login_required
@user_passes_test(block_student)
def course_list(request):
    context = {}

    module_groups = ModuleGroup.objects.all()
    courses = Course.objects.all()

    context['module_groups'] = module_groups
    context['courses'] = courses
    return render(request, 'course_list.html', context)


@login_required
@user_passes_test(block_student)
def course_delete(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.method == 'POST':
        course.delete()
        return redirect('course:course_list')
    
    context = {
        'name': course.course_name,
        'cancel_link': 'course:course_list'
    }
    return render(request, 'confirm_delete.html', context)


@login_required
@user_passes_test(block_student)
def course_add(request):
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            form = form.save()

            compress_image(form.image.path)
            return redirect('course:course_list')
    else:
        form = CourseForm(request.POST, request.FILES)

    return render(request, 'basic_info_form.html', {'form': form})


@login_required
@user_passes_test(block_student)
def course_edit(request, course_pk):
    course = get_object_or_404(Course, pk=course_pk)
    old_img_path = course.image.path

    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES, instance=course)
        if form.is_valid():

            course_info = form.save()
            compress_image(course_info.image.path)
            
            new_img_path = course.image.path

            if old_img_path != new_img_path:
                os.remove(old_img_path)

            return redirect('course:course_list')
    else:
        form = CourseForm(instance=course)
    return render(request, 'basic_info_form.html', {'form': form})


@login_required
@user_passes_test(block_student)
def course_view(request, course_pk):
    course = get_object_or_404(Course, pk=course_pk)

    return render(request, 'course_view.html', {"course" : course})

@login_required
@user_passes_test(block_student)
def quiz_list(request, course_pk):
    course = get_object_or_404(Course, pk=course_pk)
    quizzes = Quiz.objects.filter(course=course)
    
    context = {
        "course" : course,
        "quizzes" : quizzes,
    }
    return render(request, 'quiz_list.html', context)


@login_required
@user_passes_test(block_student)
def quiz_delete(request, course_pk, quiz_pk):
    quiz = get_object_or_404(Quiz, pk=quiz_pk)

    if request.method == 'POST':
        quiz.delete()
        return redirect(reverse('course:quiz_list', kwargs={'course_pk': course_pk}))
    
    context = {
        'name': quiz.quiz_title,
        'cancel_link': reverse('course:quiz_list', kwargs={'course_pk': course_pk})
    }
    return render(request, 'confirm_delete.html', context)


@login_required
@user_passes_test(block_student)
def quiz_add(request, course_pk):
    course = Course.objects.get(pk=course_pk)

    if request.method == 'POST':
        form = Quiz_Form(request.POST)

        form.instance.course = course
        form.instance.created_by = request.user
        
        if form.is_valid():
            form = form.save()
            cache.delete("last_course_detail")
            return redirect(reverse('course:quiz_list', kwargs={'course_pk': course_pk}))
    else:
        form = Quiz_Form()

    context = {
        'form': form,
        'course_pk' : course_pk
    }
    return render(request, 'quiz_form.html', context)


@login_required
@user_passes_test(block_student)
def quiz_edit(request, course_pk, quiz_pk):
    quiz = get_object_or_404(Quiz, pk= quiz_pk)

    if request.method == 'POST':
        form = Quiz_Form(request.POST, instance=quiz)

        if form.is_valid():
            form = form.save()
            cache.delete("last_course_detail")
            return redirect(reverse('course:quiz_list', kwargs={'course_pk': course_pk}))
    else:
        form = Quiz_Form(instance=quiz)

    context = {
        'form': form,
        'course_pk' : course_pk
    }
    return render(request, 'quiz_form.html', context)