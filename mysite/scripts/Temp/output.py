# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
from django.shortcuts import render
import codecs
import json
# Create your views here.
from django.http import HttpResponseRedirect, HttpResponse
from django.http import Http404
from django.template import loader
from django.shortcuts import get_object_or_404,render
# These views take parameters
from django.urls import reverse
from django.views import generic
from django.http import StreamingHttpResponse

from recomm.models import TeacherEssay,Teacher,Student,StudentEssay,Recommendation,TeacherFigure,Relation
from recomm.tools.pdf2txt import PdfTranstorm
from recomm.tools.similarity import  Similarity
from recomm.tools.NLTK_handin import Preprocess_Handin
from recomm.tools.NLTK_essays import Preprocess_Essays
from recomm.views import index_match
import pandas as pd
from pandas import DataFrame

def run():
    # 输出
    result = pd.DataFrame(columns=['学号','姓名','专业','论文题目','导师姓名','评阅人1','评阅人2'])
    studentids = []
    studentnames = []
    studentmajors = []
    studentessays = []
    studentmentors = []
    reviewteachers_1 = []
    reviewteachers_2 = []
    outputFile = 'recommendation_result_0419.csv'

    # TODO
    # 如何有效解决有多个导师的问题？
    studentessay_set = StudentEssay.objects.all()
    for i in studentessay_set:
        student = StudentEssay.objects.get(student_essay_title=i).student
        studentids.append(student.id)
        studentnames.append(student.student_name)
        studentmajors.append(student.student_major)
        studentessays.append(i.student_essay_title)

        # mentor
        relations = Relation.objects.filter(student=student)
        mentor = ''
        for j in range(len(relations)):
            if j!=0:
                mentor = mentor+" "
            mentor = mentor+str(relations[j].teacher_name)
        studentmentors.append(mentor)

        # review teachers
        recommendations = Recommendation.objects.filter(student_essay=i)
        reviewteachers_1.append(recommendations[0].recommend_teacher_name)
        reviewteachers_2.append(recommendations[1].recommend_teacher_name)


    '''
    recommendations = Recommendation.objects.all()
    for i in recommendations:
        studentessay = i.student_essay.student_essay_title
        student = StudentEssay.objects.get(student_essay_title=studentessay).student
        studentids.append(student.id)
        studentnames.append(student.student_name)
        studentmajors.append(student.student_major)
        studentessays.append(studentessay)
        # mentor
        relations = Relation.objects.filter(student=student)
        mentor = ''
        for j in range(len(relations)):
            if j!=0:
                mentor = mentor+" "
            mentor = mentor+str(relations[j].teacher_name)
        studentmentors.append(mentor)
        reviewteachers.append(i.recommend_teacher_name)
    '''
    print(len(studentids))
    print(len(studentnames))
    print(len(studentmajors))
    print(len(studentessays))
    print(len(studentmentors))
    print(len(reviewteachers_1))
    print(len(reviewteachers_2))

    result['学号'] = studentids
    result['姓名'] = studentnames
    result['专业'] = studentmajors
    result['论文题目'] = studentessays
    result['导师姓名'] = studentmentors
    result['评阅人1'] = reviewteachers_1
    result['评阅人2'] = reviewteachers_2

    result.to_csv(outputFile, index=False, encoding='utf_8_sig')
    print('ok')
    return