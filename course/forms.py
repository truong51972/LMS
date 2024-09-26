from django import forms
from .models import Course, Quiz, Question, Answer_Option, Sub_Course, Module, Sub_Module

class Course_Form(forms.ModelForm):
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

class Sub_Course_Form(forms.ModelForm):
    class Meta:
        model = Sub_Course
        fields = ['title']


class Module_Form(forms.ModelForm):
    class Meta:
        model = Module
        fields = ['title']


class Sub_Module_Form(forms.ModelForm):
    class Meta:
        model = Sub_Module
        fields = ['title', 'content_html_list', 'image_list', 'video_url']