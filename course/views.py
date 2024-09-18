from django.shortcuts import render, redirect, get_object_or_404
from module_group.models import ModuleGroup
from .forms import CourseForm
from .models import Course
import os
import cv2

# Create your views here.
def course_list(request):
    context = {}

    module_groups = ModuleGroup.objects.all()
    courses = Course.objects.all()

    context['module_groups'] = module_groups
    context['courses'] = courses
    return render(request, 'course_list.html', context)


def compress_image(image_path):
    img = cv2.imread(image_path)
    img = cv2.resize(img, (400, 300), interpolation=cv2.INTER_AREA)
    cv2.imwrite(image_path, img)


def course_add(request):
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            img = form.save()
            compress_image(img.image.path)
            return redirect('course:course_list')
    else:
        form = CourseForm()
    return render(request, 'course_form.html', {'form': form})


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