import os
import cv2

from django.shortcuts import render, redirect, get_object_or_404

from module_group.models import ModuleGroup

from .forms import CourseForm
from .models import Course

from django.contrib.auth.decorators import login_required
from main.utils.block import block_student
from django.contrib.auth.decorators import user_passes_test


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
def course_add(request):
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            course_info = form.save()
            compress_image(course_info.image.path)
            return redirect('course:course_list')
    else:
        form = CourseForm()
    return render(request, 'course_form.html', {'form': form})


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
def course_edit(request, pk):
    course = get_object_or_404(Course, pk=pk)
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
    return render(request, 'course_form.html', {'form': form})