from django.http import StreamingHttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.core.cache import cache

import json
import datetime

from ..models import *

from main.utils.request_to_server import _request


@csrf_exempt
def tab_behavior_logger(request, course_pk, course_name, quiz_pk, attempt_pk):
    if request.method == "POST":
        data = json.loads(request.body)

        attempt = get_object_or_404(Student_Quiz_Attempt, pk=attempt_pk)
        attempt.is_proctored = True

        tab_behavior = attempt.proctoring_data.get("tab_behavior", {})
        tab_behavior[len(tab_behavior)] = data

        attempt.proctoring_data["tab_behavior"] = tab_behavior

        attempt.save()

        return JsonResponse({"status": "ok"})
    return JsonResponse({"status": "error"}, status=400)


@csrf_exempt
def face_detector(request, course_pk, course_name, quiz_pk, attempt_pk):
    if request.method == "POST":
        data = json.loads(request.body)
        response = _request(api_name="face_detector", json=data).json()

        last_face_behavior_state = cache.get(
            f"face_behavior_{request.user.id}_{attempt_pk}", None
        )
        cache.set(f"face_behavior_{request.user.id}_{attempt_pk}", response, timeout=10)

        attempt = get_object_or_404(Student_Quiz_Attempt, pk=attempt_pk)
        attempt.is_proctored = True

        if (last_face_behavior_state is None) or (last_face_behavior_state != response):
            face_behavior = attempt.proctoring_data.get("face_behavior", {})

            # data_temp = response.copy()
            response["time"] = datetime.datetime.now().timestamp()

            face_behavior[len(face_behavior)] = response

            attempt.proctoring_data["face_behavior"] = face_behavior

        attempt.save()

        # print(response.json())
        return JsonResponse(response)
        # return JsonResponse({"status": "ok"})
    return JsonResponse({"status": "error"}, status=400)
