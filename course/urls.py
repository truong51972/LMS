from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static

app_name = 'course'

urlpatterns = [
    path('', views.course_list, name='course_list'),
    path('create/', views.course_add, name='course_add'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)