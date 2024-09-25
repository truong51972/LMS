from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.db.utils import IntegrityError
from django.core.cache import cache

from module_group.models import ModuleGroup

from ..models import Course, Quiz, Question, Answer_Option, Enrolled_course, Course_content
from ..forms import Course_Content_Form

from django.contrib.auth.decorators import login_required, user_passes_test


def content_list(request, course_pk):
    last_content_pk = cache.get('last_content_pk')
    cache.delete('last_content_pk')
    
    course = get_object_or_404(Course, pk=course_pk)

    contents = course.course_contents.all().order_by("content_order")

    context = {
        "last_content_pk" : last_content_pk,
        "course" : course,
        "contents": {},
    }

    for content in contents:
        lectures = content.lectures.all().order_by("order")
        quizzes = content.quizzes.all().order_by("order")
        context['contents'][content] = {
            'lectures': lectures,
            'quizzes': quizzes,
        }

    # print(context)
    return render(request, "content_management/content_list.html", context)


def content_add(request, course_pk):
    course = get_object_or_404(Course, pk=course_pk)
    num = len(course.course_contents.all()) + 1

    if request.method == 'POST':
        form = Course_Content_Form(request.POST)

        form.instance.course = course
        form.instance.content_order = num

        if form.is_valid():
            form = form.save()

            return redirect(reverse('course:content_list', kwargs={'course_pk': course_pk}))
    else:
        form = Course_Content_Form()

    context = {
        'form': form,
        'course_pk' : course_pk,
    }
    return render(request, 'content_management/content_form.html', context)


def content_edit(request, course_pk, content_pk):
    cache.set('last_content_pk', content_pk, timeout=60*5)
    course_content = get_object_or_404(Course_content, pk=content_pk)
    if request.method == 'POST':
        form = Course_Content_Form(request.POST, instance=course_content)

        if form.is_valid():
            form = form.save()

            return redirect(reverse('course:content_list', kwargs={'course_pk': course_pk}))
    else:
        form = Course_Content_Form(instance=course_content)

    context = {
        'form': form,
        'course_pk' : course_pk,
    }
    return render(request, 'content_management/content_form.html', context)


def content_delete(request, course_pk, content_pk):
    cache.set('last_content_pk', content_pk, timeout=60*5)
    course = get_object_or_404(Course, pk=course_pk)

    course_content = get_object_or_404(Course_content, pk=content_pk)
    content_num = course_content.content_order
    contents = course.course_contents.all().order_by("content_order")

    if request.method == 'POST':
        course_content.delete()
        for content in contents:
            if content.content_order > content_num:
                content.content_order -= 1
                content.save()
                
        cache.delete('last_content_pk')
        return redirect(reverse('course:content_list', kwargs={'course_pk': course_pk}))

    context = {
        'name': course_content.content_title,
        'cancel_link': reverse('course:content_list', kwargs={'course_pk': course_pk})
    }
    return render(request, 'confirm_delete.html', context)


def content_move_up(request, course_pk, content_pk):
    cache.set('last_content_pk', content_pk, timeout=60*5)
    course = get_object_or_404(Course, pk=course_pk)

    course_content = get_object_or_404(Course_content, pk=content_pk)
    content_num = course_content.content_order

    if content_num != 1:
        content = course.course_contents.filter(content_order= (content_num - 1))[0]
        content.content_order = 0
        content.save()

        course_content.content_order = (content_num - 1)
        course_content.save()

        content = course.course_contents.filter(content_order= 0)[0]
        content.content_order = content_num
        content.save()
    return redirect(reverse('course:content_list', kwargs={'course_pk': course_pk}))


def content_move_down(request, course_pk, content_pk):
    cache.set('last_content_pk', content_pk, timeout=60*5)
    course = get_object_or_404(Course, pk=course_pk)

    course_content = get_object_or_404(Course_content, pk=content_pk)
    content_num = course_content.content_order
    len_content = len(course.course_contents.all())

    if content_num != len_content:
        content = course.course_contents.filter(content_order= (content_num + 1))[0]
        content.content_order = 0
        content.save()

        course_content.content_order = (content_num + 1)
        course_content.save()

        content = course.course_contents.filter(content_order= 0)[0]
        content.content_order = content_num
        content.save()
    return redirect(reverse('course:content_list', kwargs={'course_pk': course_pk}))
