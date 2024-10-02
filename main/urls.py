from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views  # Import your views from the main app

from django.conf import settings
from django.conf.urls.static import static


app_name = 'main'

urlpatterns = [
    # Your other URL patterns
    path('', views.home, name='home'),
    # Authentication URLs
    path('login/', auth_views.LoginView.as_view(template_name='login.html', next_page='/'), name='login'),
    # path('logout/', auth_views.LogoutView.as_view(template_name='logout.html', next_page='login'), name='logout'),
    path('logout/', views.logout_view, name="logout"),
    path('run_setup/', views.run_setup, name="run_setup"),
]

