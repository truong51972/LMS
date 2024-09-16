from django.shortcuts import render, get_object_or_404, redirect
from .models import UserModule
from .forms import UserModuleForm
from module_group.models import Module, ModuleGroup
from django.contrib.auth.decorators import login_required


@login_required
def user_module_list(request):
    user_modules = UserModule.objects.all()
    module_groups = ModuleGroup.objects.all()
    modules = Module.objects.all()
    context = {
        'user_modules': user_modules,
        'module_groups': module_groups,
        'modules': modules,
    }
    return render(request, 'user_module_list.html', context)


@login_required
def user_module_create(request):
    if request.method == 'POST':
        form = UserModuleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_module:user_module_list')
    else:
        form = UserModuleForm()
    return render(request, 'user_module_form.html', {'form': form})


@login_required
def user_module_edit(request, pk):
    user_module = get_object_or_404(UserModule, pk=pk)
    if request.method == 'POST':
        form = UserModuleForm(request.POST, instance=user_module)
        if form.is_valid():
            form.save()
            return redirect('user_module:user_module_list')
    else:
        form = UserModuleForm(instance=user_module)
    return render(request, 'user_module_form.html', {'form': form, 'user_module': user_module})


@login_required
def user_module_delete(request, pk):
    user_module = get_object_or_404(UserModule, pk=pk)
    if request.method == 'POST':
        user_module.delete()
        return redirect('user_module:user_module_list')
    
    context = {
        'name': f'{user_module.user.username} ({user_module.module.module_name})',
        'cancel_link': 'user:user_list'
    }
    return render(request, 'confirm_delete.html', context)
    return render(request, 'user_module_delete.html', {'user_module': user_module})
