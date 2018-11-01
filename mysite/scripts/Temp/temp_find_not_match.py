from recomm.models import Teacher,Student,TeacherEssay,StudentEssay,Relation,TeacherFigure
from recomm.tools.pdf2txt import PdfTranstorm
from recomm.tools.NLTK_handin import Preprocess_Handin
import pandas as pd
import os
import codecs
#import slate
from pandas import DataFrame

def run():
    result = pd.DataFrame(columns=['学号', '姓名','论文题目'])
    r_id = []
    r_name = []
    r_title = []
    studentessays = pd.read_csv(os.path.join("/home/lsl/InitData/new_data", "new_studentessay_ori.csv"), sep=',',
                               encoding='utf_8_sig')
    studentessaylist = DataFrame(studentessays)
    db_studentessays = StudentEssay.objects.all()
    for i in range(len(studentessaylist['学号'])):
        id = int(studentessaylist.iloc[i,0])
        f = 0
        for j in db_studentessays:
            db_student_id = j.student.id
            if id == db_student_id:
                f = 1
        if f == 0: #没有被匹配
            r_id.append(id)
            r_name.append(studentessaylist.iloc[i,1])
            r_title.append(studentessaylist.iloc[i,2])
    result['学号'] = r_id
    result['姓名'] = r_name
    result['论文题目'] = r_title
    outputFile = 'find_notmatch_0416.csv'
    result.to_csv(outputFile, index=False, encoding='utf_8_sig')




