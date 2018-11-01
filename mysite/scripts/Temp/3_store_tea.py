from recomm.models import Teacher,Student,TeacherEssay,StudentEssay,Relation,TeacherFigure
from recomm.tools.pdf2txt import PdfTranstorm
from recomm.tools.NLTK_handin import Preprocess_Handin
import pandas as pd
import os
import codecs
#import slate
from pandas import DataFrame
from recomm.views import init_teacherfigure
def run():
   # 这里不需要再删除,只是处理新增的老师
   # Clear Database
   #print('Clear Teacher Database...')
   #Teacher.objects.all().delete()

   # Set up all teachers users
   '''
   print('Set up teacherusers...')
   teacherusers = pd.read_csv(os.path.join("/home/lsl/InitData/new_data", "add_teacher.csv"), sep=',', encoding='utf_8_sig')
   teacherlist = DataFrame(teacherusers)
   for i in range(len(teacherlist['工资号'])):
      id = teacherlist.iloc[i, 0]
      sname = teacherlist.iloc[i, 1]
      name = sname.strip()
      teacher = Teacher(id=id, teacher_name=name, teacher_password='0000')
      teacher.save()
   '''

   # clear teachers essay table
   print('Clear teacher essay table...')
   TeacherEssay.objects.all().delete()
   # init teachers' essays
   print('Initiate teacher essays...')
   teacheressays = pd.read_csv(os.path.join("/home/lsl/InitData", "TeacherEssay.csv"), sep=',', encoding='utf_8_sig')
   filenotfound = []
   for i in range(len(teacheressays['论文题目'])):
      if isinstance(teacheressays.iloc[i, 2],str): # 有论文的项才处理
         id = teacheressays.iloc[i, 0]
         sname = teacheressays.iloc[i, 1]
         name = sname.strip()
         stitle = teacheressays.iloc[i, 2]
         title = stitle.strip()

         # 已经将pdf转换成txt
         # read the essay
         #PdfTranstorm([ '-o', os.path.join("/home/lsl/InitData\TeacherEssay", name, title + '.txt'), '-t', 'text',
         #           os.path.join("/home/lsl/InitData\TeacherEssay", name, title + '.pdf')])


         # store to the database
         try:
            file = codecs.open(os.path.join("/home/lsl/InitData/TeacherEssay", name, title + '.txt'), encoding='utf-8')
            text = file.read()
         except FileNotFoundError:
            filenotfound.append(title)
         else:
            teacher = Teacher.objects.get(pk=id)
            essay = TeacherEssay(teacher=teacher, teacher_essay_title=title, teacher_essay_text=text)
            essay.save()
            print(name)
            print(title)


   for k in filenotfound:
      print(k)

   print('Init TeacherFigure Database...')
   TeacherFigure.objects.all().delete()
   init_teacherfigure()