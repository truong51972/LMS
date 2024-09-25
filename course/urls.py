from django.urls import path
from .views import course_management
from .views import course_operations
from .views import content_management
from .views import quiz_management
from .views import question_management
from .views import answer_management



app_name = 'course'

urlpatterns = [
    path('course_list', course_management.course_list, name='course_list'),

    path('course_add/', course_management.course_add, name='course_add'),
    path('course_edit/<int:course_pk>/', course_management.course_edit, name='course_edit'),
    path('course_delete/<int:course_pk>/', course_management.course_delete, name='course_delete'),
    path('<int:course_pk>/course_view/', course_management.course_view, name='course_view'),

    path('<int:course_pk>/content/list/', content_management.content_list, name='content_list'),
    path('<int:course_pk>/content/add/', content_management.content_add, name='content_add'),
    path('<int:course_pk>/content/<int:content_pk>/edit', content_management.content_edit, name='content_edit'),
    path('<int:course_pk>/content/<int:content_pk>/delete', content_management.content_delete, name='content_delete'),
    path('<int:course_pk>/content/<int:content_pk>/move_up', content_management.content_move_up, name='content_move_up'),
    path('<int:course_pk>/content/<int:content_pk>/move_down', content_management.content_move_down, name='content_move_down'),

    path('<int:course_pk>/quiz_list/', quiz_management.quiz_list, name='quiz_list'),
    path('<int:course_pk>/content/<int:content_pk>/quiz/add', quiz_management.quiz_add, name='quiz_add'),
    path('<int:course_pk>/content/<int:content_pk>/quiz/<int:quiz_pk>/detail/', quiz_management.quiz_detail, name='quiz_detail'),
    path('<int:course_pk>/content/<int:content_pk>/quiz/<int:quiz_pk>/edit/', quiz_management.quiz_edit, name='quiz_edit'),
    path('<int:course_pk>/content/<int:content_pk>/quiz/<int:quiz_pk>/delete/', quiz_management.quiz_delete, name='quiz_delete'),
    path('<int:course_pk>/content/<int:content_pk>/quiz/<int:quiz_pk>/move_up/', quiz_management.quiz_move_up, name='quiz_move_up'),
    path('<int:course_pk>/content/<int:content_pk>/quiz/<int:quiz_pk>/move_down/', quiz_management.quiz_move_down, name='quiz_move_down'),


    path('<int:course_pk>/content/<int:content_pk>/quiz/<int:quiz_pk>/question/add', question_management.question_add, name='question_add'),
    path('<int:course_pk>/content/<int:content_pk>/quiz/<int:quiz_pk>/question/<int:question_pk>/delete', question_management.question_delete, name='question_delete'),
    path('<int:course_pk>/content/<int:content_pk>/quiz/<int:quiz_pk>/question/<int:question_pk>/edit', question_management.question_edit, name='question_edit'),

    path('<int:course_pk>/content/<int:content_pk>/quiz/<int:quiz_pk>/question/<int:question_pk>/answer/add', answer_management.answer_add, name='answer_add'),
    path('<int:course_pk>/content/<int:content_pk>/quiz/<int:quiz_pk>/question/<int:question_pk>/answer/<int:answer_pk>/edit', answer_management.answer_edit, name='answer_edit'),
    path('<int:course_pk>/content/<int:content_pk>/quiz/<int:quiz_pk>/question/<int:question_pk>/answer/<int:answer_pk>/delete', answer_management.answer_delete, name='answer_delete'),
    
    
    path('<int:course_pk>', course_operations.short_link_course, name='short_link_course'),
    path('<int:course_pk>/view/<str:course_name>', course_operations.course_detail, name='course_detail'),
    path('<int:course_pk>/enroll', course_operations.course_enroll, name='course_enroll'),
]