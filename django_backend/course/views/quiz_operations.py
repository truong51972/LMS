import datetime

from django.core.cache import cache

from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.db.utils import IntegrityError

from module_group.models import ModuleGroup

from ..models import *

from django.contrib.auth.decorators import login_required
from main.utils.block import custom_user_passes_test, block_unenrolled_student

from .utils import query_all_sub_courses


@login_required
@custom_user_passes_test(
    block_unenrolled_student, "course:short_link_course", ["course_pk"]
)
def short_link_quiz_preview(request, course_pk, quiz_pk):
    course = get_object_or_404(Course, pk=course_pk)
    course_name = course.url()

    quiz = get_object_or_404(Quiz, pk=quiz_pk)

    reverse_link = reverse(
        "course:quiz_preview",
        kwargs={"course_pk": course_pk, "course_name": course_name, "quiz_pk": quiz_pk},
    )
    return redirect(reverse_link)


@login_required
@custom_user_passes_test(
    block_unenrolled_student, "course:short_link_course", ["course_pk"]
)
def quiz_preview(request, course_pk, course_name, quiz_pk):
    course = get_object_or_404(Course, pk=course_pk)
    if course_name != course.url():
        raise Http404("Incorrect course name!")

    course = get_object_or_404(Course, pk=course_pk)
    course_name = course.url()

    quiz = get_object_or_404(Quiz, pk=quiz_pk)
    num_of_questions = len(quiz.questions.all())

    attempts = list(Student_Quiz_Attempt.objects.filter(quiz=quiz, user=request.user))

    attempts.reverse()

    context = {
        "course": course,
        "num_of_questions": num_of_questions,
        "quiz": quiz,
        "attempts": attempts,
        "sub_courses": {},
    }
    query_all_sub_courses(course, context)

    return render(request, "quiz_operations/quiz_preview_view.html", context)


@login_required
@custom_user_passes_test(
    block_unenrolled_student, "course:short_link_course", ["course_pk"]
)
def short_link_do_quiz(request, course_pk, quiz_pk):
    course = get_object_or_404(Course, pk=course_pk)
    course_name = course.url()
    quiz = get_object_or_404(Quiz, pk=quiz_pk)

    if quiz.using_seb and "SEB" not in request.META.get("HTTP_USER_AGENT", ""):
        reverse_link = reverse(
            "course:short_link_quiz_preview",
            kwargs={"course_pk": course_pk, "quiz_pk": quiz_pk},
        )
        return redirect(reverse_link)

    student_quiz_attempt = Student_Quiz_Attempt.objects.create(
        user=request.user, quiz=quiz
    )
    cache.set(f"{request.user.id}_{course_pk}_{quiz_pk}", student_quiz_attempt.id)
    reverse_link = reverse(
        "course:do_quiz",
        kwargs={
            "course_pk": course_pk,
            "course_name": course_name,
            "quiz_pk": quiz_pk,
            "attempt_pk": student_quiz_attempt.id,
        },
    )
    return redirect(reverse_link)


@login_required
@custom_user_passes_test(
    block_unenrolled_student, "course:short_link_course", ["course_pk"]
)
def do_quiz(request, course_pk, course_name, quiz_pk, attempt_pk):
    course = get_object_or_404(Course, pk=course_pk)
    if course_name != course.url():
        raise Http404("Incorrect course name!")

    course = get_object_or_404(Course, pk=course_pk)
    course_name = course.url()
    quiz = get_object_or_404(Quiz, pk=quiz_pk)

    attempt_id = cache.get(f"{request.user.id}_{course_pk}_{quiz_pk}")

    reverse_link = reverse(
        "course:short_link_quiz_preview",
        kwargs={"course_pk": course_pk, "quiz_pk": quiz_pk},
    )

    if (attempt_id is None) or (attempt_id != attempt_pk):
        return redirect(reverse_link)
    else:
        student_quiz_attempt = get_object_or_404(Student_Quiz_Attempt, pk=attempt_id)

    if request.method == "POST":
        duration = round(
            datetime.datetime.now().timestamp()
            - student_quiz_attempt.attempt_date.timestamp()
        )

        cache.delete(f"{request.user.id}_{course_pk}_{quiz_pk}")
        total_mark = 0

        for question in quiz.questions.all():
            question_point = question.points
            answer_options = request.POST.getlist(f"answer_option_{question.id}")
            answer_options = [int(x) for x in answer_options]

            for answer_option in answer_options:
                Student_Answer.objects.create(
                    attempt=student_quiz_attempt,
                    question=question,
                    selected_option=Answer_Option.objects.get(pk=answer_option),
                )

            correct_answer_options_list = []
            num_answer_options = len(question.answer_options.all())

            for answer_option in question.answer_options.all():
                if answer_option.is_correct:
                    correct_answer_options_list.append(answer_option.id)

            num_correct_answer_options = len(
                list(set(correct_answer_options_list) & set(answer_options))
            )
            num_incorrect_answer_options = len(
                list(set(answer_options) - set(correct_answer_options_list))
            )

            final_score = question_point * (
                num_correct_answer_options / len(correct_answer_options_list)
            ) - question_point * (
                num_incorrect_answer_options / len(correct_answer_options_list)
            )
            final_score = max(0, min(final_score, question_point))

            total_mark += final_score

        student_quiz_attempt.duration = duration
        student_quiz_attempt.score = round(total_mark, 2)
        student_quiz_attempt.save()

        return redirect(reverse_link)

    else:
        questions = {}
        for question in quiz.questions.all():

            answer_options = {}
            for answer_option in question.answer_options.all():

                answer_options[answer_option.id] = {
                    "option_text": answer_option.option_text,
                }

            questions[question.id] = {
                "question_text": question.question_text,
                "points": question.points,
                "answer_options": answer_options,
            }

        context = {
            "course": course,
            "quiz": quiz,
            "attempt_id": attempt_id,
            "questions": questions,
            "type": "do_quiz",
            "student_quiz_attempt": student_quiz_attempt,
            "sub_courses": {},
        }
        query_all_sub_courses(course, context)

        return render(request, "quiz_operations/do_quiz_view.html", context)


@login_required
@custom_user_passes_test(
    block_unenrolled_student, "course:short_link_course", ["course_pk"]
)
def short_link_attempted_quiz_preview(request, course_pk, quiz_pk, attempt_pk):
    course = get_object_or_404(Course, pk=course_pk)
    course_name = course.url()

    quiz = get_object_or_404(Quiz, pk=quiz_pk)
    attempted_quiz = get_object_or_404(Student_Quiz_Attempt, pk=attempt_pk)

    reverse_link = reverse(
        "course:attempted_quiz_preview",
        kwargs={
            "course_pk": course_pk,
            "course_name": course_name,
            "quiz_pk": quiz_pk,
            "attempt_pk": attempt_pk,
        },
    )
    return redirect(reverse_link)


@login_required
@custom_user_passes_test(
    block_unenrolled_student, "course:short_link_course", ["course_pk"]
)
def attempted_quiz_preview(request, course_pk, course_name, quiz_pk, attempt_pk):
    course = get_object_or_404(Course, pk=course_pk)
    if course_name != course.url():
        raise Http404("Incorrect course name!")

    course = get_object_or_404(Course, pk=course_pk)
    course_name = course.url()

    quiz = get_object_or_404(Quiz, pk=quiz_pk)

    attempt = get_object_or_404(Student_Quiz_Attempt, pk=attempt_pk)
    selected_answers = attempt.answers_of_attempted_student.all()
    selected_answers_id = [
        selected_answer.selected_option.id for selected_answer in selected_answers
    ]

    correct_answer_options_id = []

    # questions = {}
    # for question in quiz.questions.all():
    #     questions[question] = question.answer_options.all()
    #     for answer in question.answer_options.all():
    #         if answer.is_correct:
    #             correct_answer_options_id.append(answer.id)

    questions = {}
    for question in quiz.questions.all():

        answer_options = {}
        for answer_option in question.answer_options.all():
            if answer_option.is_correct:
                correct_answer_options_id.append(answer_option.id)

            answer_options[answer_option.id] = {
                "option_text": answer_option.option_text,
                "is_correct": answer_option.is_correct,
                "is_selected": answer_option.id in selected_answers_id,
            }

        questions[question.id] = {
            "question_text": question.question_text,
            "points": question.points,
            "answer_options": answer_options,
        }

    context = {
        "course": course,
        "quiz": quiz,
        "questions": questions,
        "attempt": attempt,
        "sub_courses": {},
    }
    query_all_sub_courses(course, context)

    return render(request, "quiz_operations/attempted_quiz_view.html", context)
