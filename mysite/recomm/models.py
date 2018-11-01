# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
from django.db import models

class Assistant(models.Model):
    assistant_name = models.CharField(max_length=200)
    assistant_password = models.CharField(max_length=100)
    def __str__(self):
        return self.assistant_name

class Teacher(models.Model):
    teacher_name = models.CharField(max_length=200)
    teacher_password = models.CharField(max_length=100)
    def __str__(self):
        return self.teacher_name

class TeacherEssay(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    teacher_essay_title = models.CharField(max_length=200)
    teacher_essay_text = models.CharField(max_length=1000000)
    def __str__(self):
        return self.teacher_essay_title

class Student(models.Model):
    student_name = models.CharField(max_length=200)
    student_password = models.CharField(max_length=100)
    student_major = models.CharField(max_length=100,default='计算机')
    def __str__(self):
        return self.student_name

class StudentEssay(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    student_essay_title = models.CharField(max_length=200)
    student_essay_text = models.CharField(max_length=1000000)
    def __str__(self):
        return self.student_essay_title

class Recommendation(models.Model):
    student_essay = models.ForeignKey(StudentEssay, on_delete=models.CASCADE)
    recommend_teacher_id = models.IntegerField(default=0)
    recommend_teacher_name = models.CharField(max_length=200)
    def __str__(self):
        return ('student essay: ' +self.student_essay.student_essay_title + ' teacher_id: ' + str(self.recommend_teacher_id)+ 'teacher name: '+ self.recommend_teacher_name)

class TeacherFigure(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    figure = models.TextField()  # The content will be very large, so use TextField instead of CharField
    def __str__(self):
        #return self.teacher.teacher_name # This one is legal
        return self.figure

class Relation(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    teacher_id = models.IntegerField(default=0)
    teacher_name = models.CharField(max_length=200)
    def __str__(self):
        return ('student: ' +self.student.student_name + ' teacher_id: ' + str(self.teacher_id)+ 'teacher name: '+ self.teacher_name)
