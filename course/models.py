import os
from django.db import models
from unidecode import unidecode

from user.models import User


class Course(models.Model):
    course_name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True, max_length=500)
    image = models.ImageField(upload_to='images/')

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    
    def delete(self, *args, **kwargs):
        try:
            self.image.delete()
        except PermissionError:
            print('Error!')

        super().delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        if self.image:
            name, ext = os.path.splitext(self.image.name)
            new_filename = f"{unidecode(name)}{ext}"
            self.image.name = new_filename

        super().save(*args, **kwargs)

    def url(self):
        course_url = unidecode(self.course_name)
        course_url = course_url.lower()
        course_url = course_url.replace(' ', '-')

        return course_url

    def __str__(self):
        return self.course_name


class Course_content(models.Model):
    content_title = models.CharField(max_length=255)
    content_order = models.IntegerField()

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_contents')

    class Meta:
        unique_together = ('course', 'content_order')
    
    def __str__(self):
        return self.content_title
    

class Lecture(models.Model):
    lecture_title = models.CharField(max_length=255)
    content = models.TextField()

    course_content = models.ForeignKey(Course_content, on_delete=models.CASCADE, related_name='lectures')

    def __str__(self):
        return self.lecture_title


class Enrolled_course(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enrolled_course')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrolled_user')

    class Meta:
        unique_together = ('user', 'course')


class Quiz(models.Model):
    quiz_title = models.CharField(max_length=255)
    quiz_description = models.TextField(blank=True, null=True, max_length=500)
    total_mark = models.IntegerField()

    created_by = models.ForeignKey(User, on_delete= models.SET_NULL, null=True, related_name="quiz_created")
    course_content = models.ForeignKey(Course_content, on_delete=models.CASCADE, related_name='quizzes')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Question(models.Model):
    question_text = models.TextField()
    question_type = models.CharField(max_length=50)
    points = models.IntegerField()

    quiz = models.ForeignKey(Quiz, on_delete= models.CASCADE, related_name="questions")


class Answer_Option(models.Model):
    option_text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answer_options')


class Student_Quiz_Attempt(models.Model):
    score = models.IntegerField(default=0)
    attempt_date = models.DateTimeField(auto_now_add=True)
    is_proctored = models.BooleanField(default=False)
    proctoring_data = models.JSONField()

    user = models.ForeignKey(User, on_delete= models.CASCADE, related_name='attempted_quiz')
    quiz = models.ForeignKey(Quiz, on_delete= models.CASCADE, related_name='attempted_student')


class Student_Answer(models.Model):
    attempt = models.ForeignKey(Student_Quiz_Attempt, on_delete= models.CASCADE, related_name="answers_of_attempted_student")
    question = models.ForeignKey(Question, on_delete= models.CASCADE, related_name="students_answered")
    selected_option = models.ForeignKey(Answer_Option, on_delete= models.CASCADE, related_name='students_chose')


class AI_Grading(models.Model):
    feedback_text = models.TextField()
    awarded_points = models.IntegerField(default=0)

    answer = models.ForeignKey(Student_Answer, on_delete= models.CASCADE, related_name="graded_by_ai")