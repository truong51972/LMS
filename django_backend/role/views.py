from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from .models import Role
from .forms import RoleForm
from module_group.models import Module, ModuleGroup
from django.contrib.auth.decorators import login_required

from main.utils.block import block_student
from django.contrib.auth.decorators import user_passes_test


# Create your views here.
# Role views
@login_required
@user_passes_test(block_student)
def role_list(request):
    roles = Role.objects.all()
    module_groups = ModuleGroup.objects.all()
    modules = Module.objects.all()
    context = {
        'roles': roles,
        'module_groups': module_groups,
        'modules': modules,
    }
    return render(request, 'role_list.html', context)

@login_required
@user_passes_test(block_student)
def role_add(request):
    if request.method == 'POST':
        form = RoleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('role:role_list')
    else:
        form = RoleForm()
    return render(request, 'role_form.html', {'form': form})

@login_required
@user_passes_test(block_student)
def role_edit(request, pk):
    role = get_object_or_404(Role, pk=pk)
    if request.method == 'POST':
        form = RoleForm(request.POST, instance=role)
        if form.is_valid():
            form.save()
            return redirect('role:role_list')
    else:
        form = RoleForm(instance=role)
    return render(request, 'role_form.html', {'form': form})

@login_required
@user_passes_test(block_student)
def role_delete(request, pk):
    role = get_object_or_404(Role, pk=pk)
    if request.method == 'POST':
        role.delete()
        return redirect('role:role_list')
    
    context = {
        'name': role.role_name,
        'cancel_link': reverse('role:role_list')
    }
    return render(request, 'confirm_delete.html', context)