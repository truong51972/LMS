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

    path('detail/<int:course_pk>/quiz_list/delete/<int:quiz_pk>', views.quiz_delete, name='quiz_delete'),
    path('detail/<int:course_pk>/quiz_list/edit/<int:quiz_pk>', views.quiz_edit, name='quiz_edit'),
    path('detail/<int:course_pk>/quiz_list/add', views.quiz_add, name='quiz_add'),

    # path('detail/quiz/<int:pk>/<int:pk>/', views.quiz_detail, name='quiz_detail'),

]