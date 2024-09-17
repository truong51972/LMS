from django.shortcuts import render, redirect
from module_group.models import ModuleGroup
from .forms import CourseForm
from .models import Course

# Create your views here.
def course_list(request):
    context = {}

    module_groups = ModuleGroup.objects.all()
    courses = Course.objects.all()
    print(module_groups)
    print(courses)

    context['module_groups'] = module_groups
    context['courses'] = courses
    return render(request, 'course_list.html', context)

def course_add(request):
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('course:course_list')
    else:
        form = CourseForm()
    return render(request, 'course_form.html', {'form': form})