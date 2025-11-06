from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Subject(models.Model):
    title=models.CharField(max_length=200)
    slug=models.SlugField(unique=True)

class Lesson(models.Model):
    subject=models.ForeignKey(Subject,on_delete=models.CASCADE)
    teks_code=models.CharField(max_length=200,blank=True,null=True)
    title=models.CharField(max_length=200)
    description=models.TextField(blank=True)

class Exercise(models.Model):
    lesson=models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='exercises')
    question_text=models.TextField()
    correct_answer=models.CharField(max_length=200)
    #difficulty=models.IntegerField(default=1)

    def __str__(self):
        return self.question_text

class Option(models.Model):
    exercise=models.ForeignKey(Exercise,on_delete=models.CASCADE, related_name='options')
    option_text=models.CharField(max_length=200)
    is_correct=models.BooleanField(default=False)

    def __str__(self):
        return self.option_text

class StudentProgress(models.Model):
    student=models.ForeignKey(User,on_delete=models.CASCADE)
    exercise=models.ForeignKey(Exercise,on_delete=models.CASCADE)
    completed=models.BooleanField(default=False)
    selected_option=models.ForeignKey(Option,null=False,blank=False,on_delete=models.CASCADE)