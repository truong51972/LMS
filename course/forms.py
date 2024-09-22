from django import forms
from .models import Course, Quiz, Question, Answer_Option

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['course_name', 'description', 'image']


class Quiz_Form(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['quiz_title', 'quiz_description', 'total_mark']


class Question_Form(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question_text', 'question_type', 'points']


class Answer_Option_Form(forms.ModelForm):
    class Meta:
        model = Answer_Option
        fields = ['option_text', 'is_correct']