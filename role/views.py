from django.shortcuts import render, get_object_or_404, redirect
from .models import Role
from .forms import RoleForm
from module_group.models import Module, ModuleGroup

# Create your views here.
# Role views
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

def role_add(request):
    if request.method == 'POST':
        form = RoleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('role:role_list')
    else:
        form = RoleForm()
    return render(request, 'role_form.html', {'form': form})

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

def role_delete(request, pk):
    role = get_object_or_404(Role, pk=pk)
    if request.method == 'POST':
        role.delete()
        return redirect('role:role_list')
    
    context = {
        'name': role.role_name,
        'cancel_link': 'role:role_list'
    }
    return render(request, 'confirm_delete.html', context)