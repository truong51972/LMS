from django.shortcuts import render
from module_group.models import ModuleGroup, Module
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

def home(request):
    module_groups = ModuleGroup.objects.all()
    modules = Module.objects.all()

    context = {}

    if request.user.is_authenticated:
        context['user_name'] = request.user.username
        context['is_login'] = True
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