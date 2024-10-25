from django.http import Http404, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.core.cache import cache
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth.decorators import login_required, user_passes_test
from main.utils.block import block_student

from ..forms import *
from ..models import *

from user.models import User
from module_group.models import ModuleGroup

import plotly.graph_objects as go


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
        user = User.objects.get(id=user_id)
        all_attempt = all_attempted.filter(user=user).order_by("-id")
        last_attempt = all_attempt.first()
        last_attempt_per_user[last_attempt] = {"times": len(all_attempt)}

    context = {
        "module_groups": module_groups,
        "course": course,
        "sub_course": sub_course,
        "quiz": quiz,
        "last_attempt_per_user": last_attempt_per_user,
    }

    return render(request, "quiz_management/quiz_report_list.html", context)


def gen_fig_counter(proctoring_data):
    proctoring_counter = {
        behavior_key: len(behavior_value)
        for behavior_key, behavior_value in proctoring_data.items()
    }
    proctoring_counter_fig = go.Figure(
        data=[
            go.Bar(
                x=list(proctoring_counter.keys()), y=list(proctoring_counter.values())
            )
        ]
    )
    proctoring_counter_fig.update_layout(
        title={"text": "Counter", "x": 0.5, "xanchor": "center"},
        xaxis_title="Behavior",
        yaxis_title="Freqs",
    )
    proctoring_counter_div = proctoring_counter_fig.to_html(full_html=False)

    return proctoring_counter_div


def gen_fig_tab_behavior(proctoring_data, duration):
    time_start = None
    tab_behavior = {}
    for _, data in proctoring_data.get("tab_behavior", {}).items():
        time = data.get("time", 0)
        if (behavior := data.get("behavior", "")) != "focus":
            time_start = time
        else:
            tab_behavior["blur"] = tab_behavior.get("blur", 0) + (
                (time - time_start) / 1000
            )

    tab_behavior["focus"] = duration - tab_behavior.get("blur", 0)
    tab_behavior_fig = go.Figure(
        data=[
            go.Pie(labels=list(tab_behavior.keys()), values=list(tab_behavior.values()))
        ]
    )
    tab_behavior_fig.update_layout(
        title={"text": "Tab behavior", "x": 0.5, "xanchor": "center"},
    )
    tab_behavior_div = tab_behavior_fig.to_html(
        full_html=False, config={"responsive": True}
    )

    return tab_behavior_div


def gen_fig_face_behavior(proctoring_data, duration):
    face_behavior = {}
    time_start = None
    last_num_faces = None
    last_face_behavior = None

    for _, data in proctoring_data.get("face_behavior", {}).items():
        if data.get("code", "200") == "404":
            continue

        time = data.get("time", 0)
        num_faces = len([key for key, value in data.items() if key.startswith("face_")])

        if num_faces == 0:
            behavior = "no_face"
        elif num_faces == 1:
            behavior = data.get("face_0", "")
        else:
            behavior = f"{num_faces}_faces"

        if (last_num_faces == num_faces) and (last_face_behavior == behavior):
            continue

        if time_start is not None:
            face_behavior[last_face_behavior] = face_behavior.get(
                last_face_behavior, 0
            ) + (time - time_start)
            
        time_start = time
        last_face_behavior = behavior
        last_num_faces = num_faces
        
    if len(face_behavior) == 0:
        return '<h4 class="text-center">No Face Behavior Recoded!</h4>'

    face_behavior = {key: round(value, 2) for key, value in face_behavior.items()}
    face_behavior = dict(sorted(face_behavior.items(), key=lambda item: item[0]))

    other_behavior_time = sum(
        [value for key, value in face_behavior.items() if key is not last_face_behavior]
    )


    face_behavior[last_face_behavior] = (
        face_behavior.get(last_face_behavior, 0) + duration - other_behavior_time
    )
    face_behavior_fig = go.Figure(
        data=[
            go.Pie(
                labels=list(face_behavior.keys()), values=list(face_behavior.values())
            )
        ]
    )
    face_behavior_fig.update_layout(
        title={"text": "Tab behavior", "x": 0.5, "xanchor": "center"},
    )
    face_behavior_div = face_behavior_fig.to_html(
        full_html=False, config={"responsive": True}
    )

    return face_behavior_div


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

    attempts = list(Student_Quiz_Attempt.objects.filter(quiz=quiz, user=user))
    attempts.reverse()

    selected_answers = attempt.answers_of_attempted_student.all()
    selected_answers_id = [
        selected_answer.selected_option.id for selected_answer in selected_answers
    ]

    questions = {}
    for question in quiz.questions.all():
        answer_options = {}
        for answer_option in question.answer_options.all():
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

    duration = attempt.duration
    proctoring_data = attempt.proctoring_data

    proctoring_counter_div = gen_fig_counter(proctoring_data)
    tab_behavior_div = gen_fig_tab_behavior(proctoring_data, duration)
    face_behavior_div = gen_fig_face_behavior(proctoring_data, duration)

    context = {
        "module_groups": module_groups,
        "course": course,
        "sub_course": sub_course,
        "quiz": quiz,
        "attempt": attempt,
        "attempts": attempts,
        "questions": questions,
        "proctoring": {
            "proctoring_counter_div": proctoring_counter_div,
            "tab_behavior_div": tab_behavior_div,
            "face_behavior_div": face_behavior_div,
        },
    }

    return render(request, "quiz_management/quiz_report_detail.html", context)
