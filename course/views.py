import os
# import cv2
from PIL import Image

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from module_group.models import ModuleGroup

from .forms import CourseForm
from .models import Course

from quiz.forms import Quiz_Form, Question_Form, Answer_Option_Form
from quiz.models import Quiz, Question, Answer_Option

from django.contrib.auth.decorators import login_required
from main.utils.block import block_student
from django.contrib.auth.decorators import user_passes_test

from django.core.cache import cache


# def compress_image(image_path):
#     img = cv2.imread(image_path)
#     img = cv2.resize(img, (400, 225), interpolation=cv2.INTER_AREA)
#     cv2.imwrite(image_path, img)


def compress_image(image_path):
    with Image.open(image_path) as img:
        img = img.resize((400, 225), Image.Resampling.BILINEAR)
        img.save(image_path)


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
def course_delete(request, course_pk):
    course = get_object_or_404(Course, pk=course_pk)
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
    module_groups = ModuleGroup.objects.all()

    context = {
        'module_groups' : module_groups,
        "course" : course,
    }

    return render(request, 'course_view.html', context)

@login_required
@user_passes_test(block_student)
def quiz_list(request, course_pk):
    course = get_object_or_404(Course, pk=course_pk)
    module_groups = ModuleGroup.objects.all()
    quizzes = Quiz.objects.filter(course=course)
    all_questions = {}

    for quiz in quizzes:
        questions = Question.objects.filter(quiz=quiz)
        temp = {}
        for question in questions:
            answers = Answer_Option.objects.filter(question=question)
            temp[question] = answers

        all_questions[quiz.pk] = temp

    context = {
        'module_groups' : module_groups,
        "course" : course,
        "quizzes" : quizzes,
        "all_questions" : all_questions,
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
        'cancel_link': reverse('course:quiz_edit', kwargs={'course_pk': course_pk, 'quiz_pk': quiz_pk})
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
def quiz_information_edit(request, course_pk, quiz_pk):
    quiz = get_object_or_404(Quiz, pk= quiz_pk)

    if request.method == 'POST':
        form = Quiz_Form(request.POST, instance=quiz)

        if form.is_valid():
            form = form.save()
            return redirect(reverse('course:quiz_edit', kwargs={'course_pk': course_pk, 'quiz_pk': quiz_pk}))
    else:
        form = Quiz_Form(instance=quiz)

    context = {
        'form': form,
        'course_pk' : course_pk,
        'quiz_pk' : quiz_pk
    }
    return render(request, 'quiz_form.html', context)


@login_required
@user_passes_test(block_student)
def quiz_edit(request, course_pk, quiz_pk):
    module_groups = ModuleGroup.objects.all()
    course = get_object_or_404(Course, pk=course_pk)
    quiz = get_object_or_404(Quiz, pk=quiz_pk)

    questions = Question.objects.filter(quiz=quiz)
    questions_and_answers = {}

    for question in questions:
        answers = Answer_Option.objects.filter(question=question)
        questions_and_answers[question] = answers

        # 'module_groups' : module_groups,
    context = {
        "course" : course,
        "quiz" : quiz,
        "questions_and_answers" : questions_and_answers,
    }
    return render(request, 'quiz_edit.html', context)


@login_required
@user_passes_test(block_student)
def question_add(request, course_pk, quiz_pk):
    quiz = Quiz.objects.get(pk=quiz_pk)

    if request.method == 'POST':
        form = Question_Form(request.POST)

        form.instance.quiz = quiz
        
        if form.is_valid():
            form = form.save()
            Quiz.objects.get(pk=quiz_pk).save()

            return redirect(reverse('course:quiz_edit', kwargs={'course_pk': course_pk, 'quiz_pk': quiz_pk}))
    else:
        form = Question_Form()

    context = {
        'form': form,
        'course_pk' : course_pk,
        'quiz_pk' : quiz_pk,
    }
    return render(request, 'question_quiz_form.html', context)


@login_required
@user_passes_test(block_student)
def question_delete(request, course_pk, quiz_pk, question_pk):
    question = get_object_or_404(Question, pk=question_pk)

    if request.method == 'POST':
        question.delete()
        Quiz.objects.get(pk=quiz_pk).save()

        return redirect(reverse('course:quiz_edit', kwargs={'course_pk': course_pk, 'quiz_pk': quiz_pk}))
    
    context = {
        'name': question.question_text,
        'cancel_link': reverse('course:quiz_edit', kwargs={'course_pk': course_pk, 'quiz_pk': quiz_pk})
    }
    return render(request, 'confirm_delete.html', context)


@login_required
@user_passes_test(block_student)
def question_edit(request, course_pk, quiz_pk, question_pk):
    question = Question.objects.get(pk=question_pk)

    if request.method == 'POST':
        form = Question_Form(request.POST, instance=question)

        if form.is_valid():
            form = form.save()
            Quiz.objects.get(pk=quiz_pk).save()

            return redirect(reverse('course:quiz_edit', kwargs={'course_pk': course_pk, 'quiz_pk': quiz_pk}))
    else:
        form = Question_Form(instance=question)

    context = {
        'form': form,
        'course_pk' : course_pk,
        'quiz_pk' : quiz_pk,
    }
    return render(request, 'question_quiz_form.html', context)


@login_required
@user_passes_test(block_student)
def answer_add(request, course_pk, quiz_pk, question_pk):
    question = Question.objects.get(pk=question_pk)

    if request.method == 'POST':
        form = Answer_Option_Form(request.POST)

        form.instance.question = question
        
        if form.is_valid():
            form = form.save()
            Quiz.objects.get(pk=quiz_pk).save()

            return redirect(reverse('course:quiz_edit', kwargs={'course_pk': course_pk, 'quiz_pk': quiz_pk}))
    else:
        form = Answer_Option_Form()

    context = {
        'form': form,
        'course_pk' : course_pk,
        'quiz_pk' : quiz_pk,
    }
    return render(request, 'answer_quiz_form.html', context)


@login_required
@user_passes_test(block_student)
def answer_edit(request, course_pk, quiz_pk, question_pk, answer_pk):
    answer = Answer_Option.objects.get(pk=answer_pk)

    if request.method == 'POST':
        form = Answer_Option_Form(request.POST, instance=answer)

        if form.is_valid():
            form = form.save()
            Quiz.objects.get(pk=quiz_pk).save()

            return redirect(reverse('course:quiz_edit', kwargs={'course_pk': course_pk, 'quiz_pk': quiz_pk}))
    else:
        form = Answer_Option_Form(instance=answer)

    context = {
        'form': form,
        'course_pk' : course_pk,
        'quiz_pk' : quiz_pk,
    }
    return render(request, 'answer_quiz_form.html', context)


@login_required
@user_passes_test(block_student)
def answer_delete(request, course_pk, quiz_pk, question_pk, answer_pk):
    answer = get_object_or_404(Answer_Option, pk=answer_pk)

    
    if request.method == 'POST':
        answer.delete()
        Quiz.objects.get(pk=quiz_pk).save()

        return redirect(reverse('course:quiz_edit', kwargs={'course_pk': course_pk, 'quiz_pk': quiz_pk}))
    
    context = {
        'name': answer.option_text,
        'cancel_link': reverse('course:quiz_edit', kwargs={'course_pk': course_pk, 'quiz_pk': quiz_pk})
    }
    return render(request, 'confirm_delete.html', context)