from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from .models import Subject
from .forms import SubjectForm
from module_group.models import ModuleGroup

from django.http import HttpResponse
from .models import Material, Subject
from .forms import MaterialUploadForm
from django.contrib import messages


# Subject views
# def subject_list(request):
#     subjects = Subject.objects.all()
#     return render(request, 'subject_list.html', {'subjects': subjects})

def subject_list(request):
    module_groups = ModuleGroup.objects.all()
   # modules = Module.objects.all()
    subjects = Subject.objects.all()
    return render(request, 'subject_list.html', {
        'module_groups': module_groups,
      #  'modules': modules,
        'subjects': subjects,
    })


def subject_add(request):
    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('subject:subject_list')
    else:
        form = SubjectForm()
    return render(request, 'subject_form.html', {'form': form})

def subject_edit(request, pk):
    subject = get_object_or_404(Subject, pk=pk)
    if request.method == 'POST':
        form = SubjectForm(request.POST, instance=subject)
        if form.is_valid():
            form.save()
            return redirect('subject:subject_list')
    else:
        form = SubjectForm(instance=subject)
    return render(request, 'subject_form.html', {'form': form})

def subject_delete(request, pk):
    subject = get_object_or_404(Subject, pk=pk)
    if request.method == 'POST':
        subject.delete()
        return redirect('subject:subject_list')
    return render(request, 'subject_confirm_delete.html', {'subject': subject})


def delete_material(request, pk):
    material = get_object_or_404(Material, pk=pk)  # Replace Material with your model
    subject = material.subject  # Assuming material has a foreign key to subject
    if request.method == 'POST':
        material.delete()
        messages.success(request, 'Material deleted successfully.')
    return redirect('subject:materials_list', subject.pk)


def upload_material(request):
    subject_id = request.GET.get('subject')  # Get subject ID from query parameters
    subject = get_object_or_404(Subject, pk=subject_id)
    
    if request.method == 'POST':
        form = MaterialUploadForm(request.POST, request.FILES)
        if form.is_valid():
            material = form.save(commit=False)
            material.subject = subject  # Associate the material with the subject
            material.save()
            # Redirect to the materials list of the corresponding subject
            return redirect('subject:subject_materials', subject_id=subject_id)  
    else:
        form = MaterialUploadForm()
    
    return render(request, 'materials/upload_materials.html', {
        'form': form,
        'subject': subject
    })


# Display materials by subject view
def subject_materials(request, subject_id):
    subject = Subject.objects.get(pk=subject_id)
    assignments = subject.materials.filter(material_type='assignments')
    labs = subject.materials.filter(material_type='labs')
    lectures = subject.materials.filter(material_type='lectures')
    
    return render(request, 'materials/subject_materials.html', {
        'subject': subject,
        'assignments': assignments,
        'labs': labs,
        'lectures': lectures,
    })
