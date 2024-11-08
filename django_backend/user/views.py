from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from .models import User, Role
from .forms import UserForm, RoleForm
from module_group.models import Module, ModuleGroup
from django.contrib.auth.decorators import login_required

from main.utils.block import block_student
from django.contrib.auth.decorators import user_passes_test

@login_required
@user_passes_test(block_student)
def user_list(request):
    users = User.objects.all().order_by('role')
    module_groups = ModuleGroup.objects.all()
    modules = Module.objects.all()

    context = {
        'users': users,
        'module_groups': module_groups,
        'modules': modules,
    }
    return render(request, 'user_list.html', context)

@login_required
@user_passes_test(block_student)
def user_detail(request, pk):
    user = get_object_or_404(User, pk=pk)
    return render(request, 'user_detail.html', {'user': user})

@login_required
@user_passes_test(block_student)
def user_add(request):
    if request.method == 'POST':
        form = UserForm(request.POST, user_role = request.user.role.role_name)
        if form.is_valid():
            form.save()
            return redirect('user:user_list')
    else:
        form = UserForm(user_role = request.user.role.role_name)
    return render(request, 'user_form.html', {'form': form})

@login_required
@user_passes_test(block_student)
def user_edit(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user:user_list')
    else:
        form = UserForm(instance=user)
    return render(request, 'user_form.html', {'form': form})


@login_required
@user_passes_test(block_student)
def user_delete(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user.delete()
        return redirect('user:user_list')
    
    context = {
        'name': user.username,
        'cancel_link': reverse('user:user_list')
    }
    return render(request, 'confirm_delete.html', context)