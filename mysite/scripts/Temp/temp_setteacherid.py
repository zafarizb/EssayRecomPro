from recomm.models import Teacher,Student,TeacherEssay,StudentEssay,Relation,TeacherFigure
from recomm.tools.pdf2txt import PdfTranstorm
from recomm.tools.NLTK_handin import Preprocess_Handin
import pandas as pd
import os
import codecs
#import slate
from pandas import DataFrame

## 增加师生关系列表中的导师id
def run():
    ori_relationfile = pd.read_csv(os.path.join("/home/lsl/InitData/new_data", "new_relation_ori.csv"), sep=',', encoding='utf_8_sig')
    ori_relation = DataFrame(ori_relationfile)
    result = pd.DataFrame(columns=['学号','学生姓名','编号','导师姓名'])
    teacher_idlist = []
    for i in range(len(ori_relation['学号'])):
        teacher_name = str(ori_relation.iloc[i,3])
        steacher_name = teacher_name.strip()
        teacher = Teacher.objects.filter(teacher_name=steacher_name)
        if len(teacher) > 0:
            teacher_id = teacher[0].id
            teacher_idlist.append(teacher_id)
            print(ori_relation.iloc[i, 1])
        else:
            teacher_idlist.append(0)

    result['学号'] = ori_relation['学号']
    result['学生姓名'] = ori_relation['学生姓名']
    result['编号'] = teacher_idlist
    result['导师姓名'] = ori_relation['导师姓名']
    outputFile = 'new_relation.csv'
    result.to_csv(outputFile, index=False, encoding='utf_8_sig')
