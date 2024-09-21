from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from .models import TrainingProgram
from training_program_subjects.models import TrainingProgramSubjects
from .forms import TrainingProgramForm 
from training_program_subjects.forms import TrainingProgramSubjectsForm 
from module_group.models import ModuleGroup
from django.contrib.auth.decorators import login_required

from main.utils.block import block_student
from django.contrib.auth.decorators import user_passes_test


# Home view
def home(request):
    return render(request, 'home.html')

# Manage subjects in a training program
@login_required
@user_passes_test(block_student)
def manage_subjects(request, program_id):
    program = get_object_or_404(TrainingProgram, pk=program_id)
    if request.method == 'POST':
        form = TrainingProgramSubjectsForm(request.POST, instance=program)
        if form.is_valid():
            selected_subjects = form.cleaned_data['subjects']
            TrainingProgramSubjects.objects.filter(program=program).delete()
            for subject in selected_subjects:
                TrainingProgramSubjects.objects.create(program=program, subject=subject)
            return redirect('training_program_list')
    else:
        form = TrainingProgramSubjectsForm(instance=program)

    return render(request, 'manage_subjects.html', {'form': form, 'program': program})

# TrainingProgram views
@login_required
@user_passes_test(block_student)
def training_program_list(request):
    module_groups = ModuleGroup.objects.all()
    programs = TrainingProgram.objects.all()
    return render(request, 'training_program_list.html', {
        'programs': programs,
        'module_groups': module_groups,
        })

@login_required
@user_passes_test(block_student)
def training_program_add(request):
    if request.method == 'POST':
        form = TrainingProgramForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('training_program:training_program_list')
    else:
        form = TrainingProgramForm()
    return render(request, 'training_program_form.html', {'form': form})

@login_required
@user_passes_test(block_student)
def training_program_edit(request, pk):
    program = get_object_or_404(TrainingProgram, pk=pk)
    if request.method == 'POST':
        form = TrainingProgramForm(request.POST, instance=program)
        if form.is_valid():
            form.save()
            return redirect('training_program:training_program_list')
    else:
        form = TrainingProgramForm(instance=program)
    return render(request, 'training_program_form.html', {'form': form})

@login_required
@user_passes_test(block_student)
def training_program_delete(request, pk):
    program = get_object_or_404(TrainingProgram, pk=pk)
    if request.method == 'POST':
        program.delete()
        return redirect('training_program:training_program_list')
    
    context = {
        'name': program.program_name,
        'cancel_link': reverse('training_program:training_program_list')
    }
    return render(request, 'confirm_delete.html', context)