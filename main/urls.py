from django.urls import path
from django.contrib.auth import views as auth_views
from . import views  # Import your views from the main app

app_name = 'main'

urlpatterns = [
    # Your other URL patterns
    path('', views.home, name='home'),
    
    # Authentication URLs
    path('login/', auth_views.LoginView.as_view(template_name='login.html', next_page='/'), name='login'),
    # path('logout/', auth_views.LogoutView.as_view(template_name='logout.html', next_page='login'), name='logout'),
    path('logout/', views.logout_view, name="logout"),
]

