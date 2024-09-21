from django.urls import path
from . import views

app_name = 'course'

urlpatterns = [
    path('', views.course_list, name='course_list'),
    path('create/', views.course_add, name='course_add'),
    path('edit/<int:course_pk>/', views.course_edit, name='course_edit'),
    path('delete/<int:course_pk>/', views.course_delete, name='course_delete'),
    path('detail/<int:course_pk>/course_view/', views.course_view, name='course_view'),
    path('detail/<int:course_pk>/quiz_list/', views.quiz_list, name='quiz_list'),

    path('detail/<int:course_pk>/quiz_list/add', views.quiz_add, name='quiz_add'),
    path('detail/<int:course_pk>/quiz_list/<int:quiz_pk>/delete/', views.quiz_delete, name='quiz_delete'),
    path('detail/<int:course_pk>/quiz_list/<int:quiz_pk>/information_edit/', views.quiz_information_edit, name='quiz_information_edit'),
    path('detail/<int:course_pk>/quiz_list/<int:quiz_pk>/edit/', views.quiz_edit, name='quiz_edit'),

    # path('detail/<int:course_pk>/quiz_list/<int:quiz_pk>/question_list/', views.question_list, name='question_list'),

    path('detail/<int:course_pk>/quiz_list/<int:quiz_pk>/add/', views.question_add, name='question_add'),
    path('detail/<int:course_pk>/quiz_list/<int:quiz_pk>/delete/<int:question_pk>/', views.question_delete, name='question_delete'),
    path('detail/<int:course_pk>/quiz_list/<int:quiz_pk>/edit/<int:question_pk>/', views.question_edit, name='question_edit'),

    path('detail/<int:course_pk>/quiz_list/<int:quiz_pk>/add_answer/<int:question_pk>/', views.answer_add, name='answer_add'),

    path('detail/<int:course_pk>/quiz_list/<int:quiz_pk>/question/<int:question_pk>/edit_answer/<int:answer_pk>/', views.answer_edit, name='answer_edit'),
    path('detail/<int:course_pk>/quiz_list/<int:quiz_pk>/question/<int:question_pk>/delete_answer/<int:answer_pk>/', views.answer_delete, name='answer_delete'),


    # path('detail/quiz/<int:pk>/<int:pk>/', views.quiz_detail, name='quiz_detail'),

]