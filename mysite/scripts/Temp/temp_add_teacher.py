from recomm.models import Teacher,Student,TeacherEssay,StudentEssay,Relation,TeacherFigure
from recomm.tools.pdf2txt import PdfTranstorm
from recomm.tools.NLTK_handin import Preprocess_Handin
import pandas as pd
import os
import codecs
#import slate
from pandas import DataFrame

# 对照新给的名单，在原来的TeacherList上需要增加的导师名单
def run():
   # Set up all teachers users
   print('Find out new teacherusers...')
   #ori_teacherusers = pd.read_csv(os.path.join("/home/lsl/InitData", "TeacherList.csv"), sep=',', encoding='utf_8_sig')
   #ori_teacherlist = DataFrame(ori_teacherusers)
   new_teacherusers = pd.read_csv(os.path.join("/home/lsl/InitData/new_data", "new_teacherlist.csv"), sep=',', encoding='utf_8_sig')
   new_teacherlist = DataFrame(new_teacherusers)
   result = pd.DataFrame(columns=['新增老师'])
   add_teacher = []
   print(len(new_teacherlist['姓名']))
   print(len(Teacher.objects.all()))
   for i in range(len(new_teacherlist['姓名'])):
        new_name = str(new_teacherlist.iloc[i,1])
        teachers = Teacher.objects.filter(teacher_name=new_name)
        if len(teachers)==0:
            print(new_name)
            add_teacher.append(new_teacherlist['姓名'][i])

   result['新增老师'] = add_teacher
   outputFile = 'add_teacher.csv'
   result.to_csv(outputFile, index=False, encoding='utf_8_sig')
   print('ok')
