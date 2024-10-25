from course.models import Enrolled_course
from functools import wraps
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from typing import Callable, Any, List

def custom_user_passes_test(
        test_func: Callable[[Any], bool],
        url_name_space: str|None= None,
        reverse_kwarg_keys: List[str] = [],
        *decorator_args,
        **decorator_kwargs
    ):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if test_func(request.user, *args, *decorator_args, **kwargs, **decorator_kwargs):
                return view_func(request, *args, **kwargs)
            else:
                return redirect(reverse(url_name_space, kwargs= {key: kwargs[key] for key in reverse_kwarg_keys}))
        return _wrapped_view
    return decorator


def block_student(user):
    return user.role.role_name != 'Student'


def block_instructor(user):
    return user.role.role_name != 'Instructor'


def block_unenrolled_student(user, course_pk, *args, **kwargs):
    return len(user.enrolled_courses.filter(course=course_pk)) == 1


def block_by_role_name(user, roles_name: list|str, *args, **kwargs):
    for role_name in roles_name:
        if user.role.role_name == role_name:
            return False
    return True





