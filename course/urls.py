from django.urls import path
from .views import course_management
from .views import course_operations

app_name = 'course'

urlpatterns = [
    path('course_list', course_management.course_list, name='course_list'),

    path('course_add/', course_management.course_add, name='course_add'),
    path('course_edit/<int:course_pk>/', course_management.course_edit, name='course_edit'),
    path('course_delete/<int:course_pk>/', course_management.course_delete, name='course_delete'),
    path('<int:course_pk>/course_view/', course_management.course_view, name='course_view'),

    path('<int:course_pk>/quiz_list/', course_management.quiz_list, name='quiz_list'),
    path('<int:course_pk>/quiz_list/quiz_add', course_management.quiz_add, name='quiz_add'),
    path('<int:course_pk>/quiz/<int:quiz_pk>/quiz_delete/', course_management.quiz_delete, name='quiz_delete'),
    path('<int:course_pk>/quiz/<int:quiz_pk>/quiz_edit/', course_management.quiz_edit, name='quiz_edit'),
    path('<int:course_pk>/quiz/<int:quiz_pk>/quiz_detail/', course_management.quiz_detail, name='quiz_detail'),

    path('<int:course_pk>/quiz/<int:quiz_pk>/question_add/', course_management.question_add, name='question_add'),
    path('<int:course_pk>/quiz/<int:quiz_pk>/question_delete/<int:question_pk>/', course_management.question_delete, name='question_delete'),
    path('<int:course_pk>/quiz/<int:quiz_pk>/question_edit/<int:question_pk>/', course_management.question_edit, name='question_edit'),

    path('<int:course_pk>/quiz/<int:quiz_pk>/question/<int:question_pk>/answer_add', course_management.answer_add, name='answer_add'),
    path('<int:course_pk>/quiz/<int:quiz_pk>/question/<int:question_pk>/answer_edit/<int:answer_pk>/', course_management.answer_edit, name='answer_edit'),
    path('<int:course_pk>/quiz/<int:quiz_pk>/question/<int:question_pk>/answer_delete/<int:answer_pk>/', course_management.answer_delete, name='answer_delete'),
    
    
    path('<int:course_pk>', course_operations.short_link_course, name='short_link_course'),
    path('<int:course_pk>/<str:course_name>', course_operations.course, name='course'),
]