from recomm.models import Teacher,Student,TeacherEssay,StudentEssay
from recomm.tools.pdf2txt import PdfTranstorm
from recomm.tools.NLTK_handin import Preprocess_Handin
from recomm.tools.Translate import Translate
import pandas as pd
import os
import codecs
from pandas import DataFrame
import csv

# Init the students users and essays database
def run():
   print('Finding out File_Not_Found Student essays...')
   # init students' essays
   file_not_found_stuid = []
   file_not_found_title = []
   result = pd.DataFrame(columns=['学号', '论文题目'])

   studentessays = pd.read_csv(os.path.join("/home/lsl/InitData/new_data", "new_studentessay0416_01.csv"), sep=',', encoding='utf_8_sig')
   #for i in range(190,len(studentessays['论文题目'])):
   for i in range(len(studentessays['论文题目'])):
       if isinstance(studentessays.iloc[i, 2], str):  # 有论文的项才处理
           id = studentessays.iloc[i, 0]
           sname = studentessays.iloc[i, 1]
           name = sname.strip()
           stitle = studentessays.iloc[i, 2]
           title = stitle.strip()
           title = str(id)+'_'+title

       try:
           file = open( os.path.join("/home/lsl/InitData/new_data/StudentEssay", title + '.txt'), encoding='utf-8')
           file2 = open(os.path.join("/home/lsl/InitData/new_data/StudentEssay", title + '_en.txt'), encoding='utf-8')
       except FileNotFoundError:
           file_not_found_stuid.append(id)
           file_not_found_title.append(title)

   result['学号'] = file_not_found_stuid
   result['论文题目'] = file_not_found_title
   result.to_csv('not_found_stuessay.csv', index=False, encoding='utf_8_sig')
   print('ok')
