from django.http import Http404, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.core.cache import cache
from django.views.decorators.csrf import csrf_exempt

from module_group.models import ModuleGroup

from ..forms import *
from ..models import *

from user.models import User

from django.contrib.auth.decorators import login_required, user_passes_test
from main.utils.block import block_student

import json
import base64


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
    return render(request, 'quiz_management/quiz_list.html', context)


@login_required
@user_passes_test(block_student)
def quiz_delete(request, course_pk, sub_course_pk, quiz_pk):
    course = get_object_or_404(Course, pk=course_pk)
    sub_course = get_object_or_404(Sub_Course, pk=sub_course_pk)
    quiz = get_object_or_404(Quiz, pk=quiz_pk)

    if request.method == 'POST':
        order = quiz.order
        quiz.delete()
        
        quizzes = sub_course.quizzes.all().order_by("order")
        for quiz in quizzes:
            if quiz.order > order:
                quiz.order -= 1
                quiz.save()

        return redirect(reverse('course:sub_course_list', kwargs={'course_pk': course_pk}))
    
    context = {
        'name': quiz.quiz_title,
        'cancel_link': reverse('course:quiz_detail', kwargs={'course_pk': course_pk, 'sub_course_pk' : sub_course_pk,'quiz_pk': quiz_pk})
    }
    return render(request, 'confirm_delete.html', context)


@login_required
@user_passes_test(block_student)
def quiz_add(request, course_pk, sub_course_pk):
    cache.set('last_sub_course_pk', sub_course_pk, timeout=60*5)

    sub_course = get_object_or_404(Sub_Course, pk= sub_course_pk)
    num_quiz = len(sub_course.quizzes.all())

    if request.method == 'POST':
        form = Quiz_Form(request.POST)

        form.instance.sub_course = sub_course
        form.instance.created_by = request.user
        form.instance.order = num_quiz + 1
        
        if form.is_valid():
            form = form.save()
            return redirect(reverse('course:sub_course_list', kwargs={'course_pk': course_pk}))
    else:
        form = Quiz_Form()

    context = {
        'form': form,
        'course_pk' : course_pk
    }
    return render(request, 'quiz_management/quiz_form.html', context)


@login_required
@user_passes_test(block_student)
def quiz_edit(request, course_pk, sub_course_pk, quiz_pk):
    course = get_object_or_404(Course, pk=course_pk)
    content = get_object_or_404(Sub_Course, pk=sub_course_pk)
    quiz = get_object_or_404(Quiz, pk=quiz_pk)

    if request.method == 'POST':
        form = Quiz_Form(request.POST, instance=quiz)

        if form.is_valid():
            form = form.save()
            return redirect(reverse('course:quiz_detail', kwargs={'course_pk': course_pk, 'sub_course_pk' : sub_course_pk, 'quiz_pk': quiz_pk}))
    else:
        form = Quiz_Form(instance=quiz)

    context = {
        'form': form,
        'course_pk' : course_pk,
        'sub_course_pk' : sub_course_pk,
        'quiz_pk' : quiz_pk
    }
    return render(request, 'quiz_management/quiz_form.html', context)


@login_required
@user_passes_test(block_student)
def quiz_detail(request, course_pk, sub_course_pk, quiz_pk):
    cache.set('last_sub_course_pk', sub_course_pk, timeout=60*5)
    
    module_groups = ModuleGroup.objects.all()
    course = get_object_or_404(Course, pk=course_pk)
    sub_course = get_object_or_404(Sub_Course, pk=sub_course_pk)
    quiz = get_object_or_404(Quiz, pk=quiz_pk)

    questions = Question.objects.filter(quiz=quiz)
    questions_and_answers = {}

    for question in questions:
        answers = Answer_Option.objects.filter(question=question)
        questions_and_answers[question] = answers

        # 'module_groups' : module_groups,
    context = {
        "course" : course,
        "sub_course" : sub_course,
        "quiz" : quiz,
        "questions_and_answers" : questions_and_answers,
    }
    return render(request, 'quiz_management/quiz_detail.html', context)


def quiz_move_up(request, course_pk, sub_course_pk, quiz_pk):
    cache.set('last_sub_course_pk', sub_course_pk, timeout=60*5)
    sub_course = get_object_or_404(Sub_Course, pk=sub_course_pk)

    quiz = get_object_or_404(Quiz, pk=quiz_pk)
    quiz_num = quiz.order
    if quiz_num != 1:
        quiz_temp = sub_course.quizzes.filter(order= (quiz_num - 1))[0]
        quiz_temp.order = 0
        quiz_temp.save()

        quiz.order = (quiz_num - 1)
        quiz.save()

        quiz_temp = sub_course.quizzes.filter(order= 0)[0]
        quiz_temp.order = quiz_num
        quiz_temp.save()
    return redirect(reverse('course:sub_course_list', kwargs={'course_pk': course_pk}))


def quiz_move_down(request, course_pk, sub_course_pk, quiz_pk):
    cache.set('last_sub_course_pk', sub_course_pk, timeout=60*5)
    sub_course = get_object_or_404(Sub_Course, pk=sub_course_pk)

    quiz = get_object_or_404(Quiz, pk=quiz_pk)
    quiz_num = quiz.order
    num_quiz = len(sub_course.quizzes.all())

    if quiz_num != num_quiz:
        quiz_temp = sub_course.quizzes.filter(order= (quiz_num + 1))[0]
        quiz_temp.order = 0
        quiz_temp.save()

        quiz.order = (quiz_num + 1)
        quiz.save()

        quiz_temp = sub_course.quizzes.filter(order= 0)[0]
        quiz_temp.order = quiz_num
        quiz_temp.save()
    return redirect(reverse('course:sub_course_list', kwargs={'course_pk': course_pk}))


@login_required
@user_passes_test(block_student)
def quiz_report_list(request, course_pk, sub_course_pk, quiz_pk):
    course = get_object_or_404(Course, pk=course_pk)
    sub_course = get_object_or_404(Sub_Course, pk=sub_course_pk)
    quiz = get_object_or_404(Quiz, pk=quiz_pk)

    module_groups = ModuleGroup.objects.all()

    all_attempted = quiz.attempted_student.all()
    
    unique_user_ids = set([attempted.user.id for attempted in all_attempted])
    last_attempt_per_user = {}

    for user_id in unique_user_ids:
        user = User.objects.get(id= user_id)
        all_attempt = all_attempted.filter(user=user).order_by('-id')
        last_attempt = all_attempt.first()
        last_attempt_per_user[last_attempt] = {
            'times' : len(all_attempt)
        }

    context = {
        'module_groups' : module_groups,
        "course" : course,
        "sub_course" : sub_course,
        "quiz" : quiz,
        "last_attempt_per_user" : last_attempt_per_user,
    }
    
    return render(request, 'quiz_management/quiz_report_list.html', context)


@login_required
@user_passes_test(block_student)
@csrf_exempt
def quiz_report_detail(request, course_pk, sub_course_pk, quiz_pk, user_pk, attempt_pk):
    module_groups = ModuleGroup.objects.all()

    course = get_object_or_404(Course, pk=course_pk)
    sub_course = get_object_or_404(Sub_Course, pk=sub_course_pk)
    quiz = get_object_or_404(Quiz, pk=quiz_pk)
    user = get_object_or_404(User, pk=user_pk)
    attempt = get_object_or_404(Student_Quiz_Attempt, pk=attempt_pk)

    attempts = list(Student_Quiz_Attempt.objects.filter(
        quiz = quiz,
        user = request.user
    ))
    attempts.reverse()


    selected_answers = attempt.answers_of_attempted_student.all()
    selected_answers_id = [selected_answer.selected_option.id for selected_answer in selected_answers]

    correct_answer_options_id = []

    questions = {}
    for question in quiz.questions.all():
        questions[question] = question.answer_options.all()
        for answer in question.answer_options.all():
            if answer.is_correct:
                correct_answer_options_id.append(answer.id)

    context = {
        'module_groups' : module_groups,
        "course" : course,
        "sub_course" : sub_course,
        "quiz" : quiz,
        "attempt" : attempt,
        "questions": questions,
        "correct_answer_options_id": correct_answer_options_id,
        "selected_answers_id": selected_answers_id,
        "attempts" : attempts,
    }
    
    return render(request, 'quiz_management/quiz_report_detail.html', context)