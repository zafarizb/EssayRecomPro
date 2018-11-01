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
    teacher = Teacher(id=18, teacher_name='罗笑南', teacher_password='0000')
    teacher.save()
    teacher = Teacher(id=19, teacher_name='孙伟', teacher_password='0000')
    teacher.save()
    teacher = Teacher(id=20, teacher_name='王军', teacher_password='0000')
    teacher.save()
    teacher = Teacher(id=21, teacher_name='张军', teacher_password='0000')
    teacher.save()
    teacher = Teacher(id=22, teacher_name='李元新', teacher_password='0000')
    teacher.save()
    print('ok')
    '''
    18	罗笑南
19	张治国
20	孙伟
21	王军
22	张军
23	李元新

    '''