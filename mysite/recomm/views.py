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
from django.shortcuts import redirect
from django.http import JsonResponse
from django.http import StreamingHttpResponse
from .models import Assistant,TeacherEssay,Teacher,Student,StudentEssay,Recommendation,TeacherFigure,Relation
from .tools.pdf2txt import PdfTranstorm
from .tools.similarity import  Similarity
from .tools.NLTK_handin import Preprocess_Handin
from .tools.NLTK_essays import Preprocess_Essays
import pandas as pd
import zipfile
from pandas import DataFrame
import time
from time import sleep
import PyPDF2
from django.core.cache import cache
from .tools.pdf2txt import PdfTranstorm
from .tools.Translate import Translate
import pdfminer
import xlwt
import csv

def login(request):
    return render(request, 'recomm/login.html')

def logincheck(request):
    print(request.POST['username'])
    print(request.POST['password'])
    #assis = Assistant(assistant_name="admin", assistant_password='0000')
    #assis.save()
    # Check whether the assistant user and password is valid
    str1 = {'info': 'User not exists'}
    str2 = {'info': 'Teacher password not valid'}
    str3 = {'info': 'Admin password not valid'}
    try:
        assistant = Assistant.objects.get(assistant_name=request.POST['username'])
    # User not found
    except Assistant.DoesNotExist:
        # Check whether is teacher user
        try:
            teacher = Teacher.objects.get(pk=request.POST['username'])
        # User not found
        except Teacher.DoesNotExist:
            return render(request, 'recomm/login.html', {'data': json.dumps(str1)})
        password = teacher.teacher_password
        if password == request.POST['password']:
            res = HttpResponseRedirect(reverse('recomm:teacherindex', args=[teacher.id]))
            res.set_cookie('userid',request.POST['username']) # 设置cookie
            return res
        else:
            return render(request, 'recomm/login.html', {'data': json.dumps(str2)})
    password = assistant.assistant_password
    if password == request.POST['password']:
        res = HttpResponseRedirect(reverse('recomm:assistantindex', args=[3]))###重新设置
        res.set_cookie('userid', 3) # 设置cookie########################333
        return res
    else:
        return render(request, 'recomm/login.html', {'data': json.dumps(str3)}) # 通过参数告知前端进行错误提示

def assistant_userinfo(request,assistant_id):
    # cookie检查
    if (request.COOKIES['userid'] != assistant_id):
        str = {'info': 'Please log in first.'}
        return render(request, 'recomm/login.html', {'data': json.dumps(str)})  # 通过参数告知前端进行错误提示

    return render(request, 'recomm/assistant/user_info.html',{'userid':assistant_id})  # 通过参数告知前端进行错误提示

def teacher_userinfo(request,teacher_id):
    # cookie检查
    if (request.COOKIES['userid'] != teacher_id):
        str = {'info': 'Please log in first.'}
        return render(request, 'recomm/login.html', {'data': json.dumps(str)})  # 通过参数告知前端进行错误提示

    teacher = Teacher.objects.get(pk=teacher_id)
    return render(request, 'recomm/teacher/user_info.html',{'userid':teacher_id,'username':teacher.teacher_name})  # 通过参数告知前端进行错误提示


def ass_change_passwd(request,assistant_id):
    # cookie检查
    if (request.COOKIES['userid'] != assistant_id):
        str = {'info': 'Please log in first.'}
        return render(request, 'recomm/login.html', {'data': json.dumps(str)})  # 通过参数告知前端进行错误提示

    ass = Assistant.objects.get(pk=assistant_id)
    ass.assistant_password = request.POST['new_passwd']
    ass.save()
    return HttpResponse('ok')

def teacher_change_passwd(request,teacher_id):
    # cookie检查
    if (request.COOKIES['userid'] != teacher_id):
        str = {'info': 'Please log in first.'}
        return render(request, 'recomm/login.html', {'data': json.dumps(str)})  # 通过参数告知前端进行错误提示

    tch = Teacher.objects.get(pk=teacher_id)
    tch.teacher_password = request.POST['new_passwd']
    tch.save()
    return HttpResponse('ok')

# 教务员 - 首页/管理教师用户界面
def assistant_index(request,assistant_id):
    # cookie检查
    if (request.COOKIES['userid'] != assistant_id):
        str = {'info': 'Please log in first.'}
        return render(request, 'recomm/login.html', {'data': json.dumps(str)})  # 通过参数告知前端进行错误提示

    return manage_teacher(request,assistant_id)

def manage_teacher(request,assistant_id):
    # 检查cookie,若还没有登陆，则跳转到登陆页面并提示用户登陆
    if(request.COOKIES['userid']!=assistant_id):
        str = {'info': 'Please log in first.'}
        return render(request, 'recomm/login.html', {'data': json.dumps(str)}) # 通过参数告知前端进行错误提示

    teachers = []
    for i in range(len(Teacher.objects.all())):
        teacher = Teacher.objects.all()[i]
        teacheressay = TeacherEssay.objects.filter(teacher=teacher)
        essays = []
        for j in range(len(teacheressay)): # Get teacher essays
            title = teacheressay[j].teacher_essay_title
            essay = {'Essaytitle': title}
            essays.append(essay)
        t = {"id":i,"teacherid": teacher.id, "name": teacher.teacher_name, "password": teacher.teacher_password,'essay':essays}
        teachers.append(t)
    return render(request, 'recomm/assistant/index.html', {'grid_data': json.dumps(teachers),'userid':assistant_id})

# 教务员 - 管理学生用户的界面
def manage_student(request,assistant_id):
    # cookie检查
    if (request.COOKIES['userid'] != assistant_id):
        str = {'info': 'Please log in first.'}
        return render(request, 'recomm/login.html', {'data': json.dumps(str)})  # 通过参数告知前端进行错误提示

    students = []
    for i in range(len(Student.objects.all())):
        student = Student.objects.all()[i]
        studentessay = StudentEssay.objects.filter(student=student)
        essays = []
        for j in range(len(studentessay)): # Get teacher essays
            title = studentessay[j].student_essay_title
            essay = {'Essaytitle': title}
            essays.append(essay)

        # 查询导师关系
        relation = Relation.objects.filter(student=student)
        guide_teacher = ''
        for k in range(len(relation)):
            if k==1:
                guide_teacher = guide_teacher + ','
            guide = relation[k].teacher_name
            guide_teacher = guide_teacher + guide

        print(guide_teacher)
        t = {"id":i,"studentid": student.id, "name": student.student_name, "guide_teacher": guide_teacher,'essay':essays}
        students.append(t)
    return render(request, 'recomm/assistant/manage_student.html', {'grid_data': json.dumps(students),'userid':assistant_id})



# Assistant hands in students' essays
def handin_studentessay(request,assistant_id):
    return render(request, 'recomm/assistant/handin_studentessay.html', {'assistantid': assistant_id})
# Deal with Assistant hands in students' essays
def upload_studentessay(request,assistant_id):
    print('Uploading student essays...')
    # Upload the file
    if request.method == "POST":    # 请求方法为POST时，进行处理
        essay = request.FILES.get("file",None)    # 获取上传的文件,注意对应前端的name的名字，如果没有文件，则默认为None
    if essay == None:
        return HttpResponse("No files for upload!")
    destination = open(os.path.join("/home/lsl/InitData/StudentHandin",essay.name),'wb+')    # 打开特定的文件进行二进制的写操作
    for chunk in essay.chunks():      # 分块写入文件
         destination.write(chunk)
    destination.close()
    print(essay.name)

    # If zip file
    str = essay.name
    if str.find('.zip') != -1:
        f = zipfile.ZipFile(os.path.join("/home/lsl/InitData/StudentHandin",essay.name), 'r')
        # print(f.infolist())
        for file in f.namelist():
            f.extract(file, "/home/lsl/InitData/StudentHandin")
    # If not zip file
    else:
        print('pdf')
    return HttpResponse('Upload student essays.')
    # To Do
    # Get the uploaded student essays and write to the databases

# 教务员 - 设置推荐规则页面
def set_rule(request,assistant_id):
    # cookie检查
    if (request.COOKIES['userid'] != assistant_id):
        str = {'info': 'Please log in first.'}
        return render(request, 'recomm/login.html', {'data': json.dumps(str)})  # 通过参数告知前端进行错误提示

    return render(request, 'recomm/assistant/set_rule.html',{'userid':assistant_id})

def match_page(request,assistant_id):
    # cookie检查
    if (request.COOKIES['userid'] != assistant_id):
        str = {'info': 'Please log in first.'}
        return render(request, 'recomm/login.html', {'data': json.dumps(str)})  # 通过参数告知前端进行错误提示

    return render(request, 'recomm/assistant/match_page.html',{'userid':assistant_id})




def submit_rule(request,assistant_id):
    # cookie检查
    if (request.COOKIES['userid'] != assistant_id):
        str = {'info': 'Please log in first.'}
        return render(request, 'recomm/login.html', {'data': json.dumps(str)})  # 通过参数告知前端进行错误提示

    print(request.POST['state'])
    print(request.POST['spinner1'])
    print(request.POST['spinner2'])

    print('Uploading files...')
    # Upload the file
    if request.method == "POST":    # 请求方法为POST时，进行处理
        student_list = request.FILES.get("inputfile0", None)
        teacher_list = request.FILES.get("inputfile1", None)
        rule_relation = request.FILES.get("inputfile2",None)    # 获取上传的文件,注意对应前端的name的名字，如果没有文件，则默认为None
        studentessaylist = request.FILES.get("inputfile3",None)
        studentessaybag = request.FILES.get("inputfile4", None)
    if student_list == None:
            return HttpResponse("No students namelist for upload!")
    if rule_relation == None:
        return HttpResponse("No relation files for upload!")
    if studentessaylist == None:
        return HttpResponse("No studentessaylist for upload!")
    if studentessaybag == None:
        return HttpResponse("No studentessaybag for upload!")

    # 保存学生名单
    destination = open(os.path.join("/home/lsl/InitData/Input","StudentList.csv"),'wb+')    # 打开特定的文件进行二进制的写操作
    for chunk in student_list.chunks():      # 分块写入文件
         destination.write(chunk)
    destination.close()
    print(student_list.name)

    # 保存老师名单
    '''
    destination0 = open(os.path.join("/home/lsl/InitData/Input","TeacherList.csv"),'wb+')    # 打开特定的文件进行二进制的写操作
    for chunk in teacher_list.chunks():      # 分块写入文件
         destination0.write(chunk)
  
    destination0.close()

    print(teacher_list.name)
      '''
    # 保存学生导师信息csv文件
    destination1 = open(os.path.join("/home/lsl/InitData/Input/Rules","Relation.csv"),'wb+')    # 打开特定的文件进行二进制的写操作
    for chunk in rule_relation.chunks():      # 分块写入文件
         destination1.write(chunk)
    destination1.close()
    print(rule_relation.name)

    # 保存学生论文列表csv文件
    destination2 = open(os.path.join("/home/lsl/InitData/Input",studentessaylist.name),'wb+')    # 打开特定的文件进行二进制的写操作
    for chunk in studentessaylist.chunks():      # 分块写入文件
         destination2.write(chunk)
    destination2.close()
    print(studentessaylist.name)

    # 学生论文压缩包zip/rar文件
    destination3 = open(os.path.join("/home/lsl/InitData/Input",studentessaybag.name),'wb+')    # 打开特定的文件进行二进制的写操作
    for chunk in studentessaybag.chunks():      # 分块写入文件
         destination3.write(chunk)
    destination3.close()

    # 解压学生论文压缩包到StudentEssay文件夹中
    # If zip file
    str = studentessaybag.name
    if str.find('.zip') != -1:
        print('Unziping file...')
        f = zipfile.ZipFile(os.path.join("/home/lsl/InitData/Input",studentessaybag.name), 'r')
        f.extractall(path="/home/lsl/InitData/Input/StudentEssay")

    stuessay_foler = studentessaybag.name[0:len(studentessaybag.name)-4]
    stuessay_foler_path = os.path.join("/home/lsl/InitData/Input/StudentEssay",stuessay_foler)

    # 更新数据库
    # 将规则信息写到csv文件中
    review_rule = pd.DataFrame(columns=['teacher_reviewnum','student_sendnum'])
    review_rule.loc[0, 'teacher_reviewnum'] = request.POST['spinner1']
    review_rule.loc[0, 'student_sendnum'] = request.POST['spinner2']
    review_rule.to_csv(os.path.join("/home/lsl/InitData/Input/Rules","Rule.csv"),index=False, encoding='utf_8_sig')

    # 更新学生名单
    stu_path = os.path.join("/home/lsl/InitData/Input","StudentList.csv")
    init_stu(stu_path)

    # 更新老师名单
    '''
    tea_path = os.path.join("/home/lsl/InitData/Input","TeacherList.csv")
    init_tea(tea_path)
    '''

    # 更新学生导师关系
    rel_path = os.path.join("/home/lsl/InitData/Input/Rules","Relation.csv")
    init_relation(rel_path)

    # 更新学生论文（包括翻译、写入数据库等）
    stuessay_path  = os.path.join("/home/lsl/InitData/Input","StudentEssay.csv")
    print(stuessay_foler_path)
    init_stuessay(stuessay_path,stuessay_foler_path)

    # 页面跳转
    return HttpResponseRedirect(reverse('recomm:matchpage', args=(assistant_id)))

def init_stu(stu_path):
    print('Clear Student Table...')
    Student.objects.all().delete()

    # Set up all student users
    print('Set up studentusers...')
    studentusers = pd.read_csv(stu_path, sep=',',encoding='utf_8_sig')
    studentlist = DataFrame(studentusers)
    for i in range(len(studentlist['学号'])):
        id = studentlist.iloc[i, 0]
        sname = studentlist.iloc[i, 1]
        name = sname.strip()
        student = Student(id=id, student_name=name, student_password='0000')
        student.save()
        print(id)
    print('Set up students OK.')

def init_tea(tea_path):
    # Clear Database
    print('Clear Teacher Table...')
    Teacher.objects.all().delete()

    # Set up all teachers users
    print('Set up teacherusers...')
    teacherusers = pd.read_csv(tea_path, sep=',',
                               encoding='utf_8_sig')
    teacherlist = DataFrame(teacherusers)
    for i in range(len(teacherlist['姓名'])):
        id = teacherlist.iloc[i, 0]
        sname = teacherlist.iloc[i, 1]
        name = sname.strip()
        teacher = Teacher(id=id, teacher_name=name, teacher_password='0000')
        teacher.save()
        print(id)
    print('Set up teachers OK.')

def init_relation(rel_path):
    print('Clear Relation Table...')
    Relation.objects.all().delete()

    print('Set up relation...')
    studentusers = pd.read_csv(rel_path, sep=',',encoding='utf_8_sig')
    studentlist = DataFrame(studentusers)
    for i in range(len(studentlist['学号'])):
        id = studentlist.iloc[i, 0]
        student = Student.objects.get(pk=id)
        tid = studentlist.iloc[i, 2]
        tname = studentlist.iloc[i, 3]
        teachername = tname.strip()
        relation = Relation(student=student, teacher_id=tid, teacher_name=teachername)
        relation.save()
    print('Set up relation OK.')

def init_stuessay(stuessay_path,stuessay_folder_path):
    # init students' essays
    print('Delete student essays table ...')
    StudentEssay.objects.all().delete()
    print('Add student essays ...')
    studentessays = pd.read_csv(stuessay_path, sep=',',encoding='utf_8_sig')
    for i in range(len(studentessays['姓名'])):
        if isinstance(studentessays.iloc[i, 2], str):  # 有论文的项才处理
            id = studentessays.iloc[i, 0]
            sname = studentessays.iloc[i, 1]
            name = sname.strip()
            stitle = studentessays.iloc[i, 2]
            title = stitle.strip()
            # title = str(id)+'_'+title

            # transforming
            not_found = []
            type_error = []
            try:
                PdfTranstorm(['-o', os.path.join("/home/lsl/InitData/Input/StudentEssay", title + '.txt'), '-t', 'text',
                              os.path.join(stuessay_folder_path, title + '.pdf')])
            except FileNotFoundError:
                print('not found error')
                print(name)
                print(title)
                not_found.append({name: title})
            except pdfminer.pdfparser.PDFSyntaxError:
                print('type error')
                print(name)
                print(title)
                type_error.append({name: title})
            except pdfminer.pdfdocument.PDFTextExtractionNotAllowed:
                print('type error')
                print(name)
                print(title)
                type_error.append({name: title})
            except KeyError:
                print('type error')
                print(name)
                print(title)
                type_error.append({name: title})
            else:
                print(name)
                print(title)

            # translating
            ori_text_filepath = os.path.join("/home/lsl/InitData/Input/StudentEssay", title + '.txt')
            translate_text_filepath = os.path.join("/home/lsl/InitData/Input/StudentEssay", title + '_en' + '.txt')
            Translate(ori_text_filepath, translate_text_filepath)

            # read the essay
            try:
                translate_text_filepath = os.path.join("/home/lsl/InitData/Input/StudentEssay", title + '_en' + '.txt')
                translate_file = open(translate_text_filepath, encoding='utf-8')
            except FileNotFoundError:
                print('********File not found:*********')
                print(sname)
                print(title)
            else:
                translate_text = translate_file.read()

                # store to the database
                student = Student.objects.get(pk=id)
                essay = StudentEssay(student=student, student_essay_title=title, student_essay_text=translate_text)
                essay.save()
                print('#########Save file:###########')
                print(name)
                print(title)

def teacher_index(request,teacher_id):
    # cookie检查
    if (request.COOKIES['userid'] != teacher_id):
        str = {'info': 'Please log in first.'}
        return render(request, 'recomm/login.html', {'data': json.dumps(str)})  # 通过参数告知前端进行错误提示

    return teacher_checkessay(request, teacher_id)

# Teacher check essays that he handed in
def teacher_checkessay(request,teacher_id):
    # cookie检查
    if (request.COOKIES['userid'] != teacher_id):
        str = {'info': 'Please log in first.'}
        return render(request, 'recomm/login.html', {'data': json.dumps(str)})  # 通过参数告知前端进行错误提示

    if (request.COOKIES['userid'] != teacher_id):
        str = {'info': 'Please log in first.'}
        return render(request, 'recomm/login.html', {'data': json.dumps(str)})  # 通过参数告知前端进行错误提示

    teacher = Teacher.objects.get(pk=teacher_id)

    essays = TeacherEssay.objects.filter(teacher=teacher)
    grid_data = []
    for i in range(len(essays)):
        essay = essays[i]
        r = {"id":essay.id,"essay": essay.teacher_essay_title}
        grid_data.append(r)
    return render(request, 'recomm/teacher/check_essay.html', {'grid_data': json.dumps(grid_data),'userid':teacher_id,'username':teacher.teacher_name})

# Teacher edits his own essays
def edit_teacher_essay(request,teacher_id):
    # cookie检查
    if (request.COOKIES['userid'] != teacher_id):
        str = {'info': 'Please log in first.'}
        return render(request, 'recomm/login.html', {'data': json.dumps(str)})  # 通过参数告知前端进行错误提示

    print(request.POST['id'])
    TeacherEssay.objects.get(pk=request.POST['id']).delete()
    print('Delete essay.')
    return HttpResponse('Delete essay.')


def student_index(request,student_id):
    student = Student.objects.get(pk=student_id)
    return render(request, 'recomm/student/studentindex.html',{'student':student})

def edit_teacher(request,assistant_id):
    # cookie检查
    if (request.COOKIES['userid'] != assistant_id):
        str = {'info': 'Please log in first.'}
        return render(request, 'recomm/login.html', {'data': json.dumps(str)})  # 通过参数告知前端进行错误提示

    print('edit_teacher')
    print(request.body)
    print(request.POST['oper'])
    oper = request.POST['oper']
    if oper == 'edit': # id=0&teacherid=780&name=%E5%A8%84%E5%AE%9A%E4%BF%8A&password=0000&oper=edit'
        index = request.POST['id']
        teacher = Teacher.objects.all()[int(index)]
        ori_id = teacher.id
        new_id = int(request.POST['teacherid'])
        # Compare the id
        if ori_id == new_id:
            teacher.teacher_name = request.POST['name']
            teacher.teacher_password = request.POST['password']
            teacher.save()
            print('Save edited.')
        else:
            Teacher.objects.get(pk=ori_id).delete()
            Teacher.objects.create(pk=new_id,teacher_name=request.POST['name'],teacher_password=request.POST['password'])
            print('Id changed, a new teacher created.')
        #修改之后及时地在表格上显示出来
    if oper == 'add':
        Teacher.objects.create(pk=request.POST['teacherid'], teacher_name=request.POST['name'], teacher_password=request.POST['password'])
        print('New teacher added.')
    if oper == 'del':
        index = request.POST['id']
        teacher = Teacher.objects.all()[int(index)]
        ori_id = teacher.id
        Teacher.objects.get(pk=ori_id).delete()
        print('Teacher deleted.')
    return HttpResponse('edit_teacher')

def edit_student(request,assistant_id):
    # cookie检查
    if (request.COOKIES['userid'] != assistant_id):
        str = {'info': 'Please log in first.'}
        return render(request, 'recomm/login.html', {'data': json.dumps(str)})  # 通过参数告知前端进行错误提示

    print('edit_student')
    print(request.body)
    print(request.POST['oper'])
    oper = request.POST['oper']
    if oper == 'edit': # id=0&teacherid=780&name=%E5%A8%84%E5%AE%9A%E4%BF%8A&password=0000&oper=edit'
        index = request.POST['id']
        student = Student.objects.all()[int(index)]
        ori_id = student.id
        new_id = int(request.POST['studentid'])
        # Compare the id
        if ori_id == new_id:
            student.student_name = request.POST['name']
            student.student_password = request.POST['password']
            student.save()
            print('Student edited.')
        else:
            Student.objects.get(pk=ori_id).delete()
            Student.objects.create(pk=new_id,student_name=request.POST['name'],student_password=request.POST['password'])
            print('Id changed, a new student created.')
        #修改之后及时地在表格上显示出来
    if oper == 'add':
        Student.objects.create(pk=request.POST['studentid'], student_name=request.POST['name'], student_password=request.POST['password'])
        print('New student added.')
    if oper == 'del':
        index = request.POST['id']
        student = Student.objects.all()[int(index)]
        ori_id = student.id
        Student.objects.get(pk=ori_id).delete()
        print('Student deleted.')
    return HttpResponse('edit_student')


def teacher_handin(request,teacher_id):
    # cookie检查
    if (request.COOKIES['userid'] != teacher_id):
        str = {'info': 'Please log in first.'}
        return render(request, 'recomm/login.html', {'data': json.dumps(str)})  # 通过参数告知前端进行错误提示

    # Interact with the database and show the result
    try:
        teacher = Teacher.objects.get(pk=teacher_id)
        t = {'TeacherID':teacher.id,'TeacherName':teacher.teacher_name}
    except Teacher.DoesNotExist:
        raise Http404("Teacher does not exist")
    return render(request, 'recomm/teacher/teacher_handin.html', {'teacher': json.dumps(t),'userid':teacher_id,'username':teacher.teacher_name})


def teacher_upload(request,teacher_id):
    # cookie检查
    if (request.COOKIES['userid'] != teacher_id):
        str = {'info': 'Please log in first.'}
        return render(request, 'recomm/login.html', {'data': json.dumps(str)})  # 通过参数告知前端进行错误提示

    print('Uploading teacheressay...')

    teacher_name = Teacher.objects.get(pk=teacher_id).teacher_name

    # Upload the file
    if request.method == "POST":    # 请求方法为POST时，进行处理
        essay = request.FILES.get("file",None)    # 获取上传的文件,注意对应前端的name的名字，如果没有文件，则默认为None
    if essay == None:
        return HttpResponse("No files for upload!")
    destination = open(os.path.join("/home/lsl/InitData/TeacherEssay",teacher_name,essay.name),'wb+')    # 打开特定的文件进行二进制的写操作
    for chunk in essay.chunks():      # 分块写入文件
         destination.write(chunk)
    destination.close()
    essays = []
    # If zip file
    str = essay.name
    if str.find('.zip') != -1:
        print('Uploading zip file...')
        f = zipfile.ZipFile(os.path.join("/home/lsl/InitData/TeacherEssay",teacher_name,essay.name), 'r')
        i = 0
        for file in f.namelist():
            if i != 0 :
                f.extract(file, os.path.join("/home/lsl/InitData/TeacherEssay",teacher_name))
                #file example: zip/深度学习时间记录.txt
                essays.append(file)
            i = i + 1
    # If not zip file
    else:
        print('Uploading pdf file...')
        essays.append(essay.name)
    # Get all uploaded files
    for j in range(len(essays)):
        (filename, extension) = os.path.splitext(essays[j])
        print(filename)
        # Change the uploaded files to pdf form
        PdfTranstorm(['-o', os.path.join("/home/lsl/InitData/TeacherEssay",teacher_name, filename + '.txt'), '-t', 'text',
                      os.path.join("/home/lsl/InitData/TeacherEssay",teacher_name, filename+'.pdf')])

        # pdf translating

        # Store uploaded files to database
        file = open(os.path.join("/home/lsl/InitData/TeacherEssay",teacher_name, filename + '.txt'), encoding='utf-8')
        text = file.read()
        dealt_text = Preprocess_Handin(text)
        teacher = Teacher.objects.get(pk=teacher_id)
        teacher.teacheressay_set.create(teacher_essay_title=filename, teacher_essay_text=dealt_text)
    print('Upload teacher essays OK')

    return HttpResponse('Upload teacher essays.')

def teacher_downlaod_stuessay(request, teacher_id, filename):
    # cookie检查
    if (request.COOKIES['userid'] != teacher_id):
        str = {'info': 'Please log in first.'}
        return render(request, 'recomm/login.html', {'data': json.dumps(str)})  # 通过参数告知前端进行错误提示

    filename = filename+'.pdf'
    print(filename)
    response = StreamingHttpResponse(file_iterator(filename))
    response['Content-Type'] = 'application/pdf'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(filename)
    return response

def file_iterator(file_name, chunk_size=512):
    with open(os.path.join("C:/InitData/StudentEssay",file_name), 'rb') as f:
        while True:
            c = f.read(chunk_size)
            if c:
                yield c
            else:
                break

def teacher_match(request, teacher_id):
    # cookie检查
    if (request.COOKIES['userid'] != teacher_id):
        str = {'info': 'Please log in first.'}
        return render(request, 'recomm/login.html', {'data': json.dumps(str)})  # 通过参数告知前端进行错误提示

    teacher = Teacher.objects.get(pk=teacher_id)
    try:
        recommendations = Recommendation.objects.filter(recommend_teacher_id=teacher_id)
    except Recommendation.DoesNotExist:
        raise Http404("Don't need to review student essays.") # Don't need to review student essays

    grid_data = []
    for i in range(len(recommendations)):
        studentessay = recommendations[i].student_essay
        student = studentessay.student
        r = {"studentid": student.id, "studentname": student.student_name, "essay": studentessay.student_essay_title}
        grid_data.append(r)
    return render(request, 'recomm/teacher/teacher_match_result.html', {'grid_data': json.dumps(grid_data),'userid':teacher_id,'username':teacher.teacher_name})


def begin_match(request,assistant_id):
    # cookie检查
    if (request.COOKIES['userid'] != assistant_id):
        str = {'info': 'Please log in first.'}
        return render(request, 'recomm/login.html', {'data': json.dumps(str)})  # 通过参数告知前端进行错误提示

    results = index_match()

    # 最原始版本的结果查看
    '''
    students = Student.objects.all()
    studentessays = StudentEssay.objects.all()
    return render(request, 'recomm/assistant/matchresult.html', {'students':students,'studentessays': studentessays,'results':results})
    '''

    return JsonResponse({'json': "ok"})
    #return HttpResponseRedirect(reverse('recomm:checkmatchresult', args=(assistant_id)))
    #return check_matchresult(request,assistant_id)

def index_match():

    # 此处根据目前数据库情况看是否需要重建TeacherFigure
    TeacherFigure.objects.all().delete()
    init_teacherfigure()

    results = match()
    return results

def student_match(request, student_id):

    student = Student.objects.get(pk=student_id)
    studentessays = StudentEssay.objects.filter(student=student)
    return render(request, 'recomm/student/studentmatchresult.html', {'student':student,'studentessays':studentessays})

def init_teacherfigure():
    teachers = Teacher.objects.all()
    for i in teachers:
        teacher_figures(i.id)
    print('Teacher figure ok')

# Set up the database of teachers' figures
def teacher_figures(teacher_id):
    # Get all teachers' essay
    teacher = Teacher.objects.get(pk=teacher_id)
    print('Setting teacher figure...')
    print(teacher.teacher_name)
    s = ''
    essays = TeacherEssay.objects.filter(teacher_id=teacher_id)
    for i in essays:
        s = s + i.teacher_essay_text
    teacher = Teacher.objects.get(pk=teacher_id)
    teacher.teacherfigure_set.create(figure=s)
    return



num_progress = 0
'''
def process_data(request,assistant_id):
    n = 0
    for i in range(50):
        # ... 数据处理业务
        time.sleep(1)
        global num_progress # 此处需要修改全局变量
        num_progress = i / 50 * 100; # 更新后台进度值，因为想返回百分数所以乘100
    print('process_data')
    return JsonResponse({'name':"this"})
'''

def get_progress(request,assistant_id):
    # cookie检查
    if (request.COOKIES['userid'] != assistant_id):
        str = {'info': 'Please log in first.'}
        return render(request, 'recomm/login.html', {'data': json.dumps(str)})  # 通过参数告知前端进行错误提示

    print('get_progress')
    print(num_progress)
    return JsonResponse(num_progress, safe=False)


# To Do # To extend the number of teachers and students and configure the rules
# Match each student's essay with teacher and insert into the database of "Recommendation"
def match():
    # clear the recommendation table first...
    print('Clearing recommendation database...')
    Recommendation.objects.all().delete()

    # 从csv文件中读取数量限制的规则
    vpro = pd.read_csv(os.path.join("/home/lsl/InitData/Input/Rules","Rule.csv"), sep=',', encoding='utf_8_sig')
    teacher_reviewnum = vpro.loc[0,"teacher_reviewnum"]
    student_sendnum = vpro.loc[0, "student_sendnum"]

    results = {}
    # Calculate student's essay with each teacher's figure
    # teacher's essay
    teachers = Teacher.objects.all()
    figure_li = []
    teacher_li = [] # teachers' ids
    for i in range(len(teachers)):
    #for i in range(5):
        teacher = teachers[i]
    # test
        #if len(teacher.teacherfigure_set.all()[0].figure)!=0:
        if len(teacher.teacherfigure_set.all())!=0:
            figure = teacher.teacherfigure_set.all()[0].figure
            figure_li.append(figure)
            teacher_li.append(teacher.id)

    processed_figure = Preprocess_Essays(figure_li)

    # student's essay # for each studentessay, calculate the similarity between all teachers
    student_essays = StudentEssay.objects.all()
    k = 1
    for i in student_essays:
        studentessay = i.student_essay_text
        processed_studentessay = Preprocess_Handin(studentessay)
        result = Similarity(processed_studentessay, processed_figure)
        results[i.student_essay_title] = result # 将每篇学生论文和老师的论文比较相似度

        # 进度条显示(因为计算复杂度使用了大部分的处理时间）
        global num_progress
        num_progress = k / len(student_essays) * 100
        print('process data')
        print(num_progress)

        k = k + 1

    # send the studentessay to 'student_sendnum' teachers

    ## Ensure the maximum of similarity
    student_recommend = [] # Store how many recommendations the student already has
    for k in range(len(student_essays)):
        student_recommend.append(0)# The original num is 0

    for t in range(student_sendnum*len(student_essays)): # Need "student_sendnum*len(student_essays)" loops
        max = 0
        max_index = 0

        # Clear the unreasonable items
        for p in range(len(student_essays)):
            if student_recommend[p] < student_sendnum:
                # Clear until the first item is reasonable
                f = 1
                while f == 1:
                    teacher_index = results[student_essays[p].student_essay_title][0][0]
                    teacherid = teacher_li[teacher_index]
                    flag = 0

                    # TO DO
                    # Check whether is the teacher's student
                    # Read the restriction of relationships
                    # Set the model relationship is more reasonable
                    student = student_essays[p].student #一个学生可能有多个指导老师
                    r = Relation.objects.filter(student=student)
                    for i in range(len(r)):
                        t = r[i].teacher_id
                        if teacherid == t:
                            flag += 1 # The teacher is this students' teacher

                    # Check how many essays the teacher has to review
                    teacherreviewnum = len(Recommendation.objects.filter(recommend_teacher_id=teacherid))
                    if teacherreviewnum == teacher_reviewnum:
                        flag += 1

                    # delete the unreasonable item
                    if flag != 0:
                        del results[student_essays[p].student_essay_title][0]
                        print('Delete the recommendation: '+ str(results[student_essays[p].student_essay_title][0]))
                    else:
                        break

        # To find the maximum of the all recommendations
        for p in range(len(student_essays)):
            if student_recommend[p] < student_sendnum:
                similarity = results[student_essays[p].student_essay_title][0][1]
                if similarity >= max: # this teacher can review more essays
                    max = similarity
                    max_index = p
        # get the max
        max_studentessay = student_essays[max_index]
        max_teacherindex = results[max_studentessay.student_essay_title][0][0]
        max_teacherid = teacher_li[max_teacherindex]
        max_teachername = Teacher.objects.get(pk=max_teacherid).teacher_name
        max_studentessay.recommendation_set.create(recommend_teacher_id=max_teacherid, recommend_teacher_name=max_teachername)
        student_recommend[max_index] += 1
        # delete the item
        del results[max_studentessay.student_essay_title][0]
        print('Recommend OK. Delete: '+str(results[max_studentessay.student_essay_title][0]))


    print('all recommendation')
    print(Recommendation.objects.all())
    return results


    # this teacher can review more essays

# Ok
def test_json(config_filename):
    f = open(os.path.join("D://Conf",config_filename), 'r')
    conf = json.load(f)
    return conf['teacher_reviewnum']

def student_handin(request,student_id):
    # Interact with the database and show the result
    try:
        student = Student.objects.get(pk=student_id)
    except Student.DoesNotExist:
        raise Http404("Student does not exist")
    return render(request, 'recomm/student/studenthandin.html', {'student': student})

def student_upload(request,student_id):
    # Upload the file
    if request.method == "POST":    # 请求方法为POST时，进行处理
        essay = request.FILES.get("student_essay",None)    # 获取上传的文件,注意对应前端的name的名字，如果没有文件，则默认为None
    if essay == None:
        return HttpResponse("No files for upload!")
    destination = open(os.path.join("D://StudentEssay",essay.name),'wb+')    # 打开特定的文件进行二进制的写操作
    for chunk in essay.chunks():      # 分块写入文件
         destination.write(chunk)
    destination.close()

    file = open(os.path.join("D://SudentEssay", essay.name + '.txt'),encoding='utf-8' )
    text = file.read()
    dealt_text = Preprocess_Handin(text)
    # Write the filename into the database
    student = Student.objects.get(pk = student_id)
    student.studentessay_set.create(student_essay_title = essay.name,student_essay_text=dealt_text)

    # Transform the PDF file to TXT file
    (filename, extension) = os.path.splitext(essay.name)
    PdfTranstorm(['pdf2txt.py', '-o', os.path.join("D://StudentEssay",filename+'.txt'), '-t', 'text', os.path.join("D://StudentEssay",essay.name)])
    return HttpResponseRedirect(reverse('recomm:studenthandin', args=(student_id)))

# Assistant
# Check all students' handed in essays
def check_studentessay(request,assistant_id):
    # cookie检查
    if (request.COOKIES['userid'] != assistant_id):
        str = {'info': 'Please log in first.'}
        return render(request, 'recomm/login.html', {'data': json.dumps(str)})  # 通过参数告知前端进行错误提示

    students = Student.objects.all()
    return render(request, 'recomm/assistant/studentessay.html', {'students': students})

# Check all teachers' handed in essays
def check_teacheressay(request,assistant_id):
    # cookie检查
    if (request.COOKIES['userid'] != assistant_id):
        str = {'info': 'Please log in first.'}
        return render(request, 'recomm/login.html', {'data': json.dumps(str)})  # 通过参数告知前端进行错误提示

    teachers = Teacher.objects.all()
    return render(request, 'recomm/assistant/teacheressay.html', {'teachers': teachers})

# Check all students' handed in essays
def check_studentessay(request,assistant_id):
    # cookie检查
    if (request.COOKIES['userid'] != assistant_id):
        str = {'info': 'Please log in first.'}
        return render(request, 'recomm/login.html', {'data': json.dumps(str)})  # 通过参数告知前端进行错误提示

    students = Student.objects.all()
    return render(request, 'recomm/assistant/studentessay.html', {'students': students})


# Assistant Check match result
def check_matchresult(request,assistant_id):
    # cookie检查
    if (request.COOKIES['userid'] != assistant_id):
        str = {'info': 'Please log in first.'}
        return render(request, 'recomm/login.html', {'data': json.dumps(str)})  # 通过参数告知前端进行错误提示


    grid_data = []
    match_result = pd.DataFrame(columns=['studentid', 'studentname', 'essaytitle', 'teacherid', 'teachername'])
    line = 0
    for i in range(len(StudentEssay.objects.all())):
        studentessay = StudentEssay.objects.all()[i]
        student = studentessay.student
        recommendations = Recommendation.objects.filter(student_essay=studentessay)
        teachers = []
        for j in range(len(recommendations)):
            t = {"teacherid":recommendations[j].recommend_teacher_id,"teachername":recommendations[j].recommend_teacher_name}
            teachers.append(t)

            # Write the match result to csv file link for download
            match_result.loc[line, 'studentid'] = student.id
            match_result.loc[line, 'studentname'] = student.student_name
            match_result.loc[line, 'essaytitle'] = studentessay.student_essay_title
            match_result.loc[line, 'teacherid'] = recommendations[j].recommend_teacher_id
            match_result.loc[line, 'teachername'] = recommendations[j].recommend_teacher_name
            line = line + 1

        r = {"id":i,"studentid": student.id, "studentname": student.student_name, "essay": studentessay.student_essay_title,"teachers":teachers}
        grid_data.append(r)
        print('student_name '+student.student_name)


    match_result.to_csv(os.path.join("/home/lsl/InitData/Output","Result.csv"),index=False, encoding='utf_8_sig')

    # csv to xls
    resultexcel = xlwt.Workbook()
    resultsheet = resultexcel.add_sheet("result")
    csvfile = open(os.path.join("/home/lsl/InitData/Output", "Result.csv"), 'r')
    reader = csv.reader(csvfile)
    l = 0
    for line in reader:
        r = 0
        for i in line:
            resultsheet.write(l, r, i)
            r = r + 1
        l = l + 1
    resultexcel.save(os.path.join("/home/lsl/InitData/Output", "Result.xls"))
    print("OK")

    return render(request, 'recomm/assistant/match_result.html', {'grid_data': json.dumps(grid_data),'userid':assistant_id})

def download_result(request):
    filename='/home/lsl/InitData/Output/Result.xls'
    response = StreamingHttpResponse(readFile(1,filename))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(filename)
    return response

def download_fileformat_rule(request):
    filename='/home/lsl/InitData/Doc/Fileformat.docx'
    response = StreamingHttpResponse(readFile(1,filename))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(filename)
    return response

def teacher_download(request,filename):
    response = StreamingHttpResponse(readFile(0,filename))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(filename)
    return response

def student_download(request,filename):
    response = StreamingHttpResponse(readFile(1,filename))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(filename)
    return response

def readFile(index,filename, chunk_size=512):
    if index == 0:
        filepath = os.path.join("D://StudentEssay", filename)
    else:
        filepath = os.path.join("D://TeacherEssay", filename)
    with open(filepath, 'rb') as f:  # 文件路径
        while True:
            c = f.read(chunk_size)
            if c:
                yield c
            else:
                break

# currently write to local file
def teacher_deletefile(request,teacher_id,filename):
    # cookie检查
    if (request.COOKIES['userid'] != teacher_id):
        str = {'info': 'Please log in first.'}
        return render(request, 'recomm/login.html', {'data': json.dumps(str)})  # 通过参数告知前端进行错误提示

    TeacherEssay.objects.filter(teacher_essay_title=filename).delete()
    # how to delete in the file system
    return HttpResponseRedirect(reverse('recomm:teacherhandin', args=(teacher_id)))

def student_deletefile(request,student_id,filename):
    StudentEssay.objects.filter(student_essay_title=filename).delete()
    # how to delete in the file system
    return HttpResponseRedirect(reverse('recomm:studenthandin', args=(student_id)))
