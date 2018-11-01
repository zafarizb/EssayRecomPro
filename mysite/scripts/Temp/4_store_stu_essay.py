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
    # init students' essays
    print('Deleting student essays ...')
    StudentEssay.objects.all().delete()
    print('Adding student essays ...')
    studentessays = pd.read_csv(os.path.join("/home/lsl/InitData/new_data", "new_studentessay_0419.csv"), sep=',',
                                encoding='utf_8_sig')
    for i in range(len(studentessays['论文题目'])):
        if isinstance(studentessays.iloc[i, 2], str):  # 有论文的项才处理
            id = studentessays.iloc[i, 0]
            sname = studentessays.iloc[i, 1]
            name = sname.strip()
            stitle = studentessays.iloc[i, 2]
            title = stitle.strip()
            # title = str(id)+'_'+title

            # read the essay
            try:
                translate_text_filepath = os.path.join("/home/lsl/InitData/new_data/StudentEssay", title + '_en' + '.txt')
                translate_file = open(translate_text_filepath, encoding='utf-8')
            except FileNotFoundError:
                print('********File not found:*********')
                print(sname)
                print(title)
            else:
                translate_text = translate_file.read()

                # store to the database
                student = Student.objects.get(pk=id)
                essay = StudentEssay(student=student, student_essay_title=title, student_essay_text=translate_text)
                essay.save()
                print('#########Save file:###########')
                print(name)
                print(title)