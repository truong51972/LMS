from django.shortcuts import render
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

from module_group.models import ModuleGroup, Module

from .utils.create_default_accounts import create_default_accounts
from .utils.create_default_roles import create_default_roles
from .utils.create_default_module_group import create_default_module_group
from .utils.create_default_modules import create_default_modules

def home(request):
    module_groups = ModuleGroup.objects.all()
    modules = Module.objects.all()

    context = {}

    if request.user.is_authenticated:
        context['is_login'] = True
        context['user_name'] = request.user.username
        if request.user.role.role_name in ['Admin', 'Instructor']:
            context['module_groups'] = module_groups
            context['modules'] = modules
    else:
        context['is_login'] = False

    return render(request, 'home.html', context)


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