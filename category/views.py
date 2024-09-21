from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .models import Category
from .forms import CategoryForm
from module_group.models import Module, ModuleGroup
from django.contrib.auth.decorators import login_required

from main.utils.block import block_student
from django.contrib.auth.decorators import user_passes_test

# Category views
@login_required
@user_passes_test(block_student)
def category_list(request):
    categories = Category.objects.all()
    module_groups = ModuleGroup.objects.all()
    modules = Module.objects.all()

    context = {
        'categories': categories,
        'module_groups': module_groups,
        'modules': modules,
    }
    return render(request, 'category_list.html', context)

@login_required
@user_passes_test(block_student)
def category_detail(request, pk):
    category = get_object_or_404(Category, pk=pk)
    return render(request, 'category_detail.html', {'category': category})

@login_required
@user_passes_test(block_student)
def category_add(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('category:category_list')
    else:
        form = CategoryForm()
    return render(request, 'category_form.html', {'form': form})

@login_required
@user_passes_test(block_student)
def category_edit(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('category:category_list')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'category_form.html', {'form': form})

@login_required
@user_passes_test(block_student)
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        return redirect('category:category_list')
    
    context = {
        'name': category.category_name,
        'cancel_link': reverse('category:category_list')
    }
    return render(request, 'confirm_delete.html', context)
