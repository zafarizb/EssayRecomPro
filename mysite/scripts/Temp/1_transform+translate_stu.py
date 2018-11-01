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
   print('Transforming and Translating Student essays...')
   # init students' essays
   file_not_found = []

   studentessays = pd.read_csv(os.path.join("/home/lsl/InitData/new_data", "new_studentessay_0419.csv"), sep=',', encoding='utf_8_sig')
   #for i in range(190,len(studentessays['论文题目'])):
   for i in range(len(studentessays['论文题目'])):
       if isinstance(studentessays.iloc[i, 1], str):  # 有论文的项才处理
           id = studentessays.iloc[i, 0]
           sname = studentessays.iloc[i, 1]
           name = sname.strip()
           stitle = studentessays.iloc[i, 2] #############
           title = stitle.strip()
           ori_text_filepath = os.path.join("/home/lsl/InitData/new_data/StudentEssay", title + '.txt')
           translate_text_filepath = os.path.join("/home/lsl/InitData/new_data/StudentEssay", title + '_en' + '.txt')
           Translate(ori_text_filepath, translate_text_filepath)
           print(name)
           print(title)
'''
           try:
           # read the essay
                PdfTranstorm(['-o', os.path.join("/home/lsl/InitData/new_data/StudentEssay", title + '.txt'), '-t', 'text',
                         os.path.join("/home/lsl/InitData/new_data/StudentEssay", title + '.pdf')])
           except FileNotFoundError:
                print("*******file not found***********")
                print({name:title})
                file_not_found.append({name:title})
                row = [name,title]
                out = open(os.path.join("/home/lsl/InitData/new_data", 'not_found_studentessay.csv'), "a", newline="")
                csv_writer = csv.writer(out, dialect="excel")
                csv_writer.writerow(row)
           else:
           # translate students' essays
           
                ori_text_filepath = os.path.join("/home/lsl/InitData/new_data/StudentEssay", title + '.txt')
                translate_text_filepath = os.path.join("/home/lsl/InitData/new_data/StudentEssay", title + '_en' + '.txt')
                Translate(ori_text_filepath, translate_text_filepath)
                print(name)
                print(title)
                
'''
