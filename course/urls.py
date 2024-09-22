from django.urls import path
from . import views

app_name = 'course'

urlpatterns = [
    path('course_list', views.course_list, name='course_list'),

    path('course_add/', views.course_add, name='course_add'),
    path('course_edit/<int:course_pk>/', views.course_edit, name='course_edit'),
    path('course_delete/<int:course_pk>/', views.course_delete, name='course_delete'),

    path('<int:course_pk>/course_view/', views.course_view, name='course_view'),
    path('<int:course_pk>/quiz_list/', views.quiz_list, name='quiz_list'),
    path('<int:course_pk>/quiz_list/quiz_add', views.quiz_add, name='quiz_add'),

    path('<int:course_pk>/quiz/<int:quiz_pk>/quiz_delete/', views.quiz_delete, name='quiz_delete'),
    path('<int:course_pk>/quiz/<int:quiz_pk>/quiz_edit/', views.quiz_edit, name='quiz_edit'),
    path('<int:course_pk>/quiz/<int:quiz_pk>/quiz_detail/', views.quiz_detail, name='quiz_detail'),

    path('<int:course_pk>/quiz/<int:quiz_pk>/question_add/', views.question_add, name='question_add'),
    path('<int:course_pk>/quiz/<int:quiz_pk>/question_delete/<int:question_pk>/', views.question_delete, name='question_delete'),
    path('<int:course_pk>/quiz/<int:quiz_pk>/question_edit/<int:question_pk>/', views.question_edit, name='question_edit'),

    path('<int:course_pk>/quiz/<int:quiz_pk>/question/<int:question_pk>/answer_add', views.answer_add, name='answer_add'),
    path('<int:course_pk>/quiz/<int:quiz_pk>/question/<int:question_pk>/answer_edit/<int:answer_pk>/', views.answer_edit, name='answer_edit'),
    path('<int:course_pk>/quiz/<int:quiz_pk>/question/<int:question_pk>/answer_delete/<int:answer_pk>/', views.answer_delete, name='answer_delete'),
]