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
    # Set up the relationships between students and teachers
    '''
    print('Set up relations...')
    relationships = pd.read_csv(os.path.join("/home/lsl/InitData", "Relation.csv"), sep=',', encoding='utf_8_sig')
    relationlist = DataFrame(relationships)
    #######################################
    for i in range(len(relationlist['学号'])):
        sid = relationlist.iloc[i, 0]
        tid = relationlist.iloc[i, 2]
        name = relationlist.iloc[i, 3]
        tname = name.strip()
        student = Student.objects.get(pk=sid)
        relation = Relation(student=student, teacher_id=tid, teacher_name=tname)
        relation.save()
    '''
    ###########此处看情况是否需要删掉原来的情况
    # Clear the result matched before
    print('Delete Recommendations...')
    Recommendation.objects.all().delete()
    print('Delete Recommendations OK.')

    # begin match
    # Notice: directly get students' translated version
    print('Begin matching...')
    index_match()
    print('Match OK.')
    # 此处不能删除原来的Recommendation

    return
