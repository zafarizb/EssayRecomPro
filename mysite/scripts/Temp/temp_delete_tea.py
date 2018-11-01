from recomm.models import Teacher,Student,TeacherEssay,StudentEssay,Relation
from recomm.tools.pdf2txt import PdfTranstorm
from recomm.tools.NLTK_handin import Preprocess_Handin
import pandas as pd
import os
import codecs
#import slate
from pandas import DataFrame

def run():
   # Clear Database
   print('Delete teachers not in the list...')

   teacherusers = pd.read_csv(os.path.join("/home/lsl/InitData/new_data", "new_teacherlist.csv"), sep=',', encoding='utf_8_sig')
   teacherlist = DataFrame(teacherusers)
   all_teachers = Teacher.objects.all()
   for t in all_teachers:
       tname = t.teacher_name
       flag = 0
       for i in range(len(teacherlist['姓名'])):
            sname = str(teacherlist.iloc[i, 1])
            name = sname.strip()
            if tname == name:
                flag = 1
       if flag == 0:
           #在数据库中删除该老师
           Teacher.objects.get(teacher_name=tname).delete()
           print('delete teacher:')
           print(tname)
   print('ok')

