from recomm.models import Teacher,Student,TeacherEssay,StudentEssay,Relation
from recomm.tools.pdf2txt import PdfTranstorm
from recomm.tools.NLTK_handin import Preprocess_Handin
from recomm.tools.Translate import Translate
import pandas as pd
import os
import codecs
from pandas import DataFrame

# Init the students users and essays database
def run():
   #print('Clear Student Database...')
   #Student.objects.all().delete()

   # Set up all student users
   print('Setting up relation...')
   studentusers = pd.read_csv(os.path.join("/home/lsl/InitData/new_data", "new_relation.csv"), sep=',', encoding='utf_8_sig')
   studentlist = DataFrame(studentusers)
   for i in range(len(studentlist['学号'])):
      id = studentlist.iloc[i, 0]
      student = Student.objects.get(pk=id)
      tid = studentlist.iloc[i,2]
      tname = studentlist.iloc[i,3]
      teachername = tname.strip()
      relation = Relation(student=student,teacher_id=tid,teacher_name=teachername)
      relation.save()
   print('Setting up relation ok.')