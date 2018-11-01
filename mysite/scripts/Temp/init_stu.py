from recomm.models import Teacher,Student,TeacherEssay,StudentEssay
from recomm.tools.pdf2txt import PdfTranstorm
from recomm.tools.NLTK_handin import Preprocess_Handin
from recomm.tools.Translate import Translate
import pandas as pd
import os
import codecs
from pandas import DataFrame

# Init the students users and essays database
def run():
   print('Clear Student Database...')
   Student.objects.all().delete()

   # Set up all student users
   print('Set up studentusers...')
   studentusers = pd.read_csv(os.path.join("/home/lsl/InitData\Input\TestData", "StudentList.csv"), sep=',', encoding='utf_8_sig')
   studentlist = DataFrame(studentusers)
   for i in range(len(studentlist['学号'])):
      id = studentlist.iloc[i, 0]
      sname = studentlist.iloc[i, 1]
      name = sname.strip()
      student = Student(id=id, student_name=name, student_password='0000')
      student.save()

   # init students' essays
   StudentEssay.objects.all().delete()
   print('Initiate student essays ...')
   studentessays = pd.read_csv(os.path.join("/home/lsl/InitData\Input\TestData", "StudentEssay.csv"), sep=',', encoding='utf_8_sig')
   for i in range(len(studentessays['论文题目'])):
      if isinstance(studentessays.iloc[i, 2],str): # 有论文的项才处理
         id = studentessays.iloc[i, 0]
         sname = studentessays.iloc[i, 1]
         name = sname.strip()
         stitle = studentessays.iloc[i, 2]
         title = stitle.strip()
         # read the essay
         '''
         PdfTranstorm([ '-o', os.path.join("/home/lsl/InitData\Input\TestData", title + '.txt'), '-t', 'text',
                    os.path.join("/home/lsl/InitData\TestData", title + '.pdf')])
         '''
         # translate students' essays
         ori_text_filepath = os.path.join("/home/lsl/InitData\Input\TestData", title + '.txt')
         translate_text_filepath = os.path.join("/home/lsl/InitData\Input\TestData", title + '_en' + '.txt')
         Translate(ori_text_filepath,translate_text_filepath)

         translate_file = open(translate_text_filepath,encoding='utf-8')
         translate_text = translate_file.read()

         # store to the database
         student = Student.objects.get(pk=id)
         essay = StudentEssay(student=student, student_essay_title=title, student_essay_text=translate_text)
         essay.save()
         print('****Save to database:****')
         print(name)
         print(title)

