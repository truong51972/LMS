from django.db import models

from course.models import Course
from user.models import User

class Quiz(models.Model):
    course = models.ForeignKey(Course, on_delete= models.CASCADE)
    quiz_title = models.CharField(max_length=255)
    quiz_description = models.TextField(blank=True, null=True, max_length=500)
    total_mark = models.IntegerField()
    created_by = models.ForeignKey(User, on_delete= models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete= models.CASCADE)
    question_text = models.TextField()
    question_type = models.CharField(max_length=50)
    points = models.IntegerField()


class Answer_Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    option_text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)


class Student_Quiz_Attempt(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    quiz_id = models.ForeignKey(Quiz, on_delete= models.CASCADE)
    score = models.IntegerField(default=0)
    attempt_date = models.DateTimeField(auto_now_add=True)
    is_proctored = models.BooleanField(default=False)
    proctoring_data = models.JSONField()


class Student_Answer(models.Model):
    attempt = models.ForeignKey(Student_Quiz_Attempt, on_delete= models.CASCADE)
    question = models.ForeignKey(Question, on_delete= models.CASCADE)
    selected_option_id = models.ForeignKey(Answer_Option, on_delete= models.CASCADE)


class AI_Grading(models.Model):
    answer_id = models.ForeignKey(Student_Answer, on_delete= models.CASCADE)
    feedback_text = models.TextField()
    awarded_points = models.IntegerField(default=0)