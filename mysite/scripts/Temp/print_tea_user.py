from recomm.models import Teacher,Student,TeacherEssay,StudentEssay,Relation,TeacherFigure,Recommendation
from recomm.tools.pdf2txt import PdfTranstorm
from recomm.tools.NLTK_handin import Preprocess_Handin
import pandas as pd
import os
import codecs
#import slate
from pandas import DataFrame

# 对照新给的名单，在原来的TeacherList上需要增加的导师名单
def run():
    result = pd.DataFrame(columns=['老师','评阅论文数量'])

    db_teacher = []
    review_nums = []
    teachcers = Teacher.objects.all()
    for i in teachcers:
        db_teacher.append(i.teacher_name)
        recommendations = Recommendation.objects.filter(recommend_teacher_name=i.teacher_name)
        review_nums.append(len(recommendations))
    result['老师'] = db_teacher
    result['评阅论文数量'] = review_nums
    outputFile = 'teacher_reviewnum_0416.csv'
    result.to_csv(outputFile, index=False, encoding='utf_8_sig')
    print('ok')