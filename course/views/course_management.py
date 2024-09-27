"""
    Creating, modifying, and deleting courses or course parts
"""
import os
import shutil
import random
from PIL import Image
import pandas as pd

from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from module_group.models import ModuleGroup

from ..forms import Course_Form, Quiz_Form, Question_Form, Answer_Option_Form
from ..models import Course, Sub_Course, Module, Sub_Module, Quiz, Question, Answer_Option

from django.contrib.auth.decorators import login_required, user_passes_test
from main.utils.block import block_student

from django.contrib import messages

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
        form = Course_Form(request.POST, request.FILES)
        if form.is_valid():
            form = form.save()

            compress_image(form.image.path)
            return redirect('course:course_list')
    else:
        form = Course_Form(request.POST, request.FILES)

    return render(request, 'course_management/basic_info_form.html', {'form': form})


@login_required
@user_passes_test(block_student)
def course_edit(request, course_pk):
    course = get_object_or_404(Course, pk=course_pk)
    old_img_path = course.image.path

    if request.method == 'POST':
        form = Course_Form(request.POST, request.FILES, instance=course)
        if form.is_valid():

            course_info = form.save()
            compress_image(course_info.image.path)
            
            new_img_path = course.image.path

            if old_img_path != new_img_path:
                try:
                    os.remove(old_img_path)
                except FileNotFoundError:
                    pass

            return redirect(reverse('course:course_view', kwargs={'course_pk': course_pk}))
    else:
        form = Course_Form(instance=course)
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


def upload_existed_course(request):
    if request.method == "POST":
        csv_file = request.FILES['csv_file']
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'File không phải là định dạng CSV.')
            return redirect('course:upload_existed_course')
        lorem_text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec fringilla ultricies laoreet. Donec lacinia blandit purus ut ultricies. Fusce quis consequat risus. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas."

        df = pd.read_csv(csv_file)

        image_file_path = f"images/default_image_{random.randint(0,10000000)}.jpg"
        
        for index, row in df.iterrows():
            course_name = row.iloc[0]
            sub_course_title = row.iloc[1]
            module_title = row.iloc[2]
            sub_module_title = row.iloc[3]
            content_html_list = row.iloc[4]
            image_list = row.iloc[5]
            video_url = row.iloc[6]

            course, created = Course.objects.get_or_create(course_name= course_name, defaults={"image": image_file_path, "description": lorem_text})

            if created is False:
                shutil.copy("data/images/default_image.jpg", "media/" + image_file_path)

            order = len(course.sub_courses.all()) + 1
            sub_course, _ = Sub_Course.objects.get_or_create(title= sub_course_title, defaults={"course": course, "order": order})

            order = len(sub_course.modules.all()) + 1
            module, _ = Module.objects.get_or_create(title= module_title, defaults={"sub_course": sub_course, "order": order, "created_by": request.user})
            
            order = len(module.sub_modules.all()) + 1
            sub_module, _ = Sub_Module.objects.get_or_create(title= sub_module_title, defaults={"module": module, "order": order, "content_html_list": str(content_html_list), "image_list": image_list, "video_url": video_url})

        return redirect('course:course_list')
    
    return render(request, 'upload_existed_course_form.html')