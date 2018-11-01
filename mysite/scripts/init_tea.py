from recomm.models import Teacher,Student,TeacherEssay,StudentEssay,Relation,TeacherFigure
from recomm.tools.pdf2txt import PdfTranstorm
from recomm.tools.NLTK_handin import Preprocess_Handin
from recomm.tools.Translate import Translate
from recomm.views import init_teacherfigure
import pandas as pd
import os
import codecs
#import slate
from pandas import DataFrame
import json

def run():
   type_error = []
   # Clear Database
   print('Clear Database...')
   Teacher.objects.all().delete()

   # Set up all teachers users
   print('Set up teacherusers...')
   teacherusers = pd.read_csv(os.path.join("/home/lsl/InitData/Input", "TeacherList.csv"), sep=',', encoding='utf_8_sig')
   teacherlist = DataFrame(teacherusers)
   for i in range(len(teacherlist['工资号'])):
      id = teacherlist.iloc[i, 0]
      sname = teacherlist.iloc[i, 1]
      name = sname.strip()
      teacher = Teacher(id=id, teacher_name=name, teacher_password='0000')
      teacher.save()

   # init teachers' essays
   print('Initiate teacher essays...')
   teacheressays = pd.read_csv(os.path.join("/home/lsl/InitData/Input", "TeacherEssay.csv"), sep=',', encoding='utf_8_sig')
   for i in range(len(teacheressays['论文题目'])):
      if isinstance(teacheressays.iloc[i, 2],str): # 有论文的项才处理
         id = teacheressays.iloc[i, 0]
         sname = teacheressays.iloc[i, 1]
         name = sname.strip()
         stitle = teacheressays.iloc[i, 2]
         title = stitle.strip()
         # read the essay
         '''
         PdfTranstorm([ '-o', os.path.join("/home/lsl/InitData/TeacherEssay", name, title + '.txt'), '-t', 'text',
                    os.path.join("/home/lsl/InitData/TeacherEssay", name, title + '.pdf')])
         '''
         # translate teachers' essays
         '''
         ori_text_filepath = os.path.join("/home/lsl/InitData/TeacherEssay", name, title + '.txt')
         translate_text_filepath = os.path.join("/home/lsl/InitData/TeacherEssay", name, title + '_en' + '.txt')
         try:
            Translate(ori_text_filepath, translate_text_filepath)
         except json.decoder.JSONDecodeError:
            type_error.append(({name: title}))
            print('****Type error:****')
            print(name)
            print(title)
         else:
            print('****Translate OK:****')
            print(name)
            print(title)
         '''

         # store to the database
         #file = codecs.open(os.path.join("/home/lsl/InitData/TeacherEssay", name, title + '_en' + '.txt'), encoding='utf-8')
         file = codecs.open(os.path.join("/home/lsl/InitData/TeacherEssay", name, title + '.txt'),encoding='utf-8')
         text = file.read()

         teacher = Teacher.objects.get(pk=id)
         essay = TeacherEssay(teacher=teacher, teacher_essay_title=title, teacher_essay_text=text)
         essay.save()
         print('****Save essay:****')
         print(name)
         print(title)




