from django.shortcuts import render, get_object_or_404, redirect
from .models import Question, Answer
from .forms import QuestionForm, AnswerForm
from module_group.models import ModuleGroup
from django.utils import timezone
# Question views
def question_list(request):
    module_groups = ModuleGroup.objects.all()
    
    questions = Question.objects.all()
    
    questions_and_correct_answers = {}

    for question in questions:
        correct_answers = Answer.objects.filter(question_id = question.id, is_correct= True)
        
        questions_and_correct_answers[question.id] = {
            'question' : question,
            'correct_answers' : correct_answers
        }

    print(questions_and_correct_answers)
    context = {
        'questions': questions,
        'module_groups': module_groups,
        'correct_answers': None,
        'questions_and_correct_answers': questions_and_correct_answers,
    }
    return render(request, 'question_list.html', context)

def question_detail(request, pk):
    question = get_object_or_404(Question, pk=pk)
    return render(request, 'question_detail.html', {'question': question})

def question_add(request):
    if request.method == 'POST':
        question_form = QuestionForm(request.POST)
        if question_form.is_valid():
            question = question_form.save()
            answer_texts = request.POST.getlist('answer_text[]')
            is_position_corrects = request.POST.getlist('is_correct[]')

            is_corrects = [False]*len(answer_texts)

            for is_position_correct in is_position_corrects:
                is_corrects[int(is_position_correct)] = True
     
            for i in range(len(answer_texts)):
                Answer.objects.create(
                    question=question,
                    text=answer_texts[i],
                    is_correct=is_corrects[i]
                )

            return redirect('/question')
    else:
        question_form = QuestionForm()
    return render(request, 'question_add.html', {'question_form': question_form})

def question_edit(request, pk):
    question = get_object_or_404(Question, pk=pk)
    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            form.save()
            return redirect('question_list')
    else:
        form = QuestionForm(instance=question)
    return render(request, 'question_form.html', {'form': form})

def question_delete(request, pk):
    question = get_object_or_404(Question, pk=pk)
    if request.method == 'POST':
        question.delete()
        return redirect('question:question_list')
    
    context = {
        'name': question.question_text,
        'cancel_link': 'question:question_list'
    }
    return render(request, 'confirm_delete.html', context)
