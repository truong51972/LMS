from django.shortcuts import render
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

from module_group.models import ModuleGroup, Module
from course.models import Course

from .utils.create_default_accounts import create_default_accounts
from .utils.create_default_roles import create_default_roles
from .utils.create_default_module_group import create_default_module_group
from .utils.create_default_modules import create_default_modules

def home(request):
    if not request.user.is_authenticated:
        return render(request, 'home_not_logged.html')

    context = {}
    
    context['user_name'] = request.user.username

    role_name = request.user.role.role_name
    # if role_name in ['Admin', 'Instructor']:
    #     context['module_groups'] = ModuleGroup.objects.all()
    #     context['modules'] = Module.objects.all()

    #     return render(request, 'home.html', context)

    # else:
    #     context['courses'] = Course.objects.all()
    #     # print(context)
    #     return render(request, 'home_student.html', context)

    context['module_groups'] = ModuleGroup.objects.all()
    context['modules'] = Module.objects.all()


    context['courses'] = Course.objects.all()
    # print(context)
    return render(request, 'home_student.html', context)



def base_view(request):
    module_groups = ModuleGroup.objects.all()
    modules = Module.objects.all()
    return render(request, 'base.html', {
        'module_groups': module_groups,
        'modules': modules,
    })

def logout_view(request):
    logout(request)
    return redirect('/')

def run_setup(request):

    create_default_module_group()
    create_default_modules()
    create_default_roles()
    create_default_accounts()

    return redirect('/')