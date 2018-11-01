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
   studentusers = pd.read_csv(os.path.join("/home/lsl/InitData/new_data", "new_studentlist.csv"), sep=',', encoding='utf_8_sig')
   studentlist = DataFrame(studentusers)
   for i in range(len(studentlist['学号'])):
      id = studentlist.iloc[i, 0]
      sname = studentlist.iloc[i, 1]
      smajor = studentlist.iloc[i,2]
      name = sname.strip()
      major = smajor.strip()
      student = Student(id=id, student_name=name, student_password='0000',student_major=major)
      student.save()