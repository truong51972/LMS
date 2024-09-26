from django.urls import path
from .views import course_management
from .views import sub_course_management
from .views import module_management
from .views import sub_module_management
from .views import quiz_management
from .views import question_management
from .views import answer_management
from .views import course_operations



app_name = 'course'

urlpatterns = [
    path('course_list', course_management.course_list, name='course_list'),

    path('course_add/', course_management.course_add, name='course_add'),
    path('course_edit/<int:course_pk>/', course_management.course_edit, name='course_edit'),
    path('course_delete/<int:course_pk>/', course_management.course_delete, name='course_delete'),
    path('<int:course_pk>/course_view/', course_management.course_view, name='course_view'),

    path('<int:course_pk>/sub_course/list/', sub_course_management.sub_course_list, name='sub_course_list'),
    path('<int:course_pk>/sub_course/add/', sub_course_management.sub_course_add, name='sub_course_add'),
    path('<int:course_pk>/sub_course/<int:sub_course_pk>/edit', sub_course_management.sub_course_edit, name='sub_course_edit'),
    path('<int:course_pk>/sub_course/<int:sub_course_pk>/delete', sub_course_management.sub_course_delete, name='sub_course_delete'),
    path('<int:course_pk>/sub_course/<int:sub_course_pk>/move_up', sub_course_management.sub_course_move_up, name='sub_course_move_up'),
    path('<int:course_pk>/sub_course/<int:sub_course_pk>/move_down', sub_course_management.sub_course_move_down, name='sub_course_move_down'),

    path('<int:course_pk>/sub_course/<int:sub_course_pk>/module/add', module_management.module_add, name='module_add'),
    path('<int:course_pk>/sub_course/<int:sub_course_pk>/module/<int:module_pk>/edit', module_management.module_edit, name='module_edit'),
    path('<int:course_pk>/sub_course/<int:sub_course_pk>/module/<int:module_pk>/delete', module_management.module_delete, name='module_delete'),
    path('<int:course_pk>/sub_course/<int:sub_course_pk>/module/<int:module_pk>/move_up', module_management.module_move_up, name='module_move_up'),
    path('<int:course_pk>/sub_course/<int:sub_course_pk>/module/<int:module_pk>/move_down', module_management.module_move_down, name='module_move_down'),

    path('<int:course_pk>/sub_course/<int:sub_course_pk>/module/<int:module_pk>/sub_module/add', sub_module_management.sub_module_add, name='sub_module_add'),
    path('<int:course_pk>/sub_course/<int:sub_course_pk>/module/<int:module_pk>/sub_module/<int:sub_module_pk>/edit', sub_module_management.sub_module_edit, name='sub_module_edit'),
    path('<int:course_pk>/sub_course/<int:sub_course_pk>/module/<int:module_pk>/sub_module/<int:sub_module_pk>/delete', sub_module_management.sub_module_delete, name='sub_module_delete'),

    path('<int:course_pk>/sub_course/<int:sub_course_pk>/quiz/add', quiz_management.quiz_add, name='quiz_add'),
    path('<int:course_pk>/sub_course/<int:sub_course_pk>/quiz/<int:quiz_pk>/detail/', quiz_management.quiz_detail, name='quiz_detail'),
    path('<int:course_pk>/sub_course/<int:sub_course_pk>/quiz/<int:quiz_pk>/edit/', quiz_management.quiz_edit, name='quiz_edit'),
    path('<int:course_pk>/sub_course/<int:sub_course_pk>/quiz/<int:quiz_pk>/delete/', quiz_management.quiz_delete, name='quiz_delete'),
    path('<int:course_pk>/sub_course/<int:sub_course_pk>/quiz/<int:quiz_pk>/move_up/', quiz_management.quiz_move_up, name='quiz_move_up'),
    path('<int:course_pk>/sub_course/<int:sub_course_pk>/quiz/<int:quiz_pk>/move_down/', quiz_management.quiz_move_down, name='quiz_move_down'),


    path('<int:course_pk>/sub_course/<int:sub_course_pk>/quiz/<int:quiz_pk>/question/add', question_management.question_add, name='question_add'),
    path('<int:course_pk>/sub_course/<int:sub_course_pk>/quiz/<int:quiz_pk>/question/<int:question_pk>/delete', question_management.question_delete, name='question_delete'),
    path('<int:course_pk>/sub_course/<int:sub_course_pk>/quiz/<int:quiz_pk>/question/<int:question_pk>/edit', question_management.question_edit, name='question_edit'),

    path('<int:course_pk>/sub_course/<int:sub_course_pk>/quiz/<int:quiz_pk>/question/<int:question_pk>/answer/add', answer_management.answer_add, name='answer_add'),
    path('<int:course_pk>/sub_course/<int:sub_course_pk>/quiz/<int:quiz_pk>/question/<int:question_pk>/answer/<int:answer_pk>/edit', answer_management.answer_edit, name='answer_edit'),
    path('<int:course_pk>/sub_course/<int:sub_course_pk>/quiz/<int:quiz_pk>/question/<int:question_pk>/answer/<int:answer_pk>/delete', answer_management.answer_delete, name='answer_delete'),
    
    
    path('<int:course_pk>', course_operations.short_link_course, name='short_link_course'),
    path('<int:course_pk>/view/<str:course_name>', course_operations.course_detail, name='course_detail'),
    path('<int:course_pk>/enroll', course_operations.course_enroll, name='course_enroll'),
]