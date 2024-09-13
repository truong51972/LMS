from django.shortcuts import render, get_object_or_404, redirect
from .models import User, Role
from .forms import UserForm, RoleForm
from module_group.models import Module, ModuleGroup

# User views
def user_list(request):
    users = User.objects.all()
    module_groups = ModuleGroup.objects.all()
    modules = Module.objects.all()

    context = {
        'users': users,
        'module_groups': module_groups,
        'modules': modules,
    }
    return render(request, 'user_list.html', context)

def user_detail(request, pk):
    user = get_object_or_404(User, pk=pk)
    return render(request, 'user_detail.html', {'user': user})

def user_add(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user:user_list')
    else:
        form = UserForm()
    return render(request, 'user_form.html', {'form': form})

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


def user_delete(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user.delete()
        return redirect('user:user_list')
    
    context = {
        'name': user.username,
        'cancel_link': 'user:user_list'
    }
    return render(request, 'confirm_delete.html', context)