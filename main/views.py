from django.shortcuts import render
from module_group.models import ModuleGroup, Module
from django.contrib.auth import logout
from django.shortcuts import redirect

def home(request):
    module_groups = ModuleGroup.objects.all()
    modules = Module.objects.all()
    return render(request, 'home.html', {
        'module_groups': module_groups,
        'modules': modules,
    })


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