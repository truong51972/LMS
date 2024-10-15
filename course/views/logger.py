from django.http import StreamingHttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from ..models import *

import json

@csrf_exempt
def tab_behavior_logger(request, course_pk, course_name, quiz_pk, attempt_pk):
    if request.method == "POST":
        data = json.loads(request.body)
        
        attempt = get_object_or_404(Student_Quiz_Attempt, pk= attempt_pk)

        attempt.is_proctored= True

        tab_behavior = attempt.proctoring_data.get("tab_behavior", {})
        tab_behavior[len(tab_behavior)] = data

        attempt.proctoring_data["tab_behavior"] = tab_behavior

        attempt.save()

        return JsonResponse({"status": "ok"})
    return JsonResponse({"status": "error"}, status=400)