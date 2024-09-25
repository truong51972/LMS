"""
    Creating, modifying, and deleting courses or course parts
"""
import os
from PIL import Image

from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from module_group.models import ModuleGroup

from ..forms import CourseForm, Quiz_Form, Question_Form, Answer_Option_Form
from ..models import Course, Quiz, Question, Answer_Option

from django.contrib.auth.decorators import login_required, user_passes_test
from main.utils.block import block_student


def compress_image(image_path):
    with Image.open(image_path) as img:
        img = img.resize((800, 450), Image.Resampling.BILINEAR)
        img.save(image_path)


@login_required
@user_passes_test(block_student)
def course_list(request):
    context = {}

    module_groups = ModuleGroup.objects.all()
    courses = Course.objects.all()

    context['module_groups'] = module_groups
    context['courses'] = courses
    return render(request, 'course_management/course_list.html', context)


@login_required
@user_passes_test(block_student)
def course_delete(request, course_pk):
    course = get_object_or_404(Course, pk=course_pk)
    if request.method == 'POST':
        course.delete()
        return redirect('course:course_list')
    
    context = {
        'name': course.course_name,
        'cancel_link': reverse('course:course_list')
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

    return render(request, 'course_management/basic_info_form.html', {'form': form})


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

            return redirect(reverse('course:course_view', kwargs={'course_pk': course_pk}))
    else:
        form = CourseForm(instance=course)
    return render(request, 'course_management/basic_info_form.html', {'form': form})


@login_required
@user_passes_test(block_student)
def course_view(request, course_pk):
    course = get_object_or_404(Course, pk=course_pk)
    
    module_groups = ModuleGroup.objects.all()

    context = {
        'module_groups' : module_groups,
        "course" : course,
    }

    return render(request, 'course_management/course_view.html', context)