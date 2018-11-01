from recomm.models import Teacher,Student,TeacherEssay,StudentEssay
from recomm.tools.pdf2txt import PdfTranstorm
from recomm.tools.NLTK_handin import Preprocess_Handin
from recomm.tools.Translate import Translate
import pandas as pd
import os
import codecs
from pandas import DataFrame
import json

def run():
    type_error = []
    # Translate teachers' essays
    print('Translating teacher essays...')
    teacheressays = pd.read_csv(os.path.join("/home/lsl/InitData/new_data", "add_teacheressay.csv"), sep=',', encoding='utf_8_sig')
    for i in range(len(teacheressays['论文题目'])):
        if isinstance(teacheressays.iloc[i, 2], str):  # 有论文的项才处理
            id = teacheressays.iloc[i, 0]
            sname = teacheressays.iloc[i, 1]
            name = sname.strip()
            stitle = teacheressays.iloc[i, 2]
            title = stitle.strip()


        # translate teachers' essays
        ori_text_filepath = os.path.join("/home/lsl/InitData\TeacherEssay", name, title + '.txt')
        translate_text_filepath = os.path.join("/home/lsl/InitData\TeacherEssay", name, title + '_en' + '.txt')
        try:
            Translate(ori_text_filepath, translate_text_filepath)
        except json.decoder.JSONDecodeError:
            type_error.append(({name:title}))
            print('****Type error:****')
            print(name)
            print(title)
        else:
            print(name)
            print(title)

    for i in range(len(type_error)):
        print(type_error[i])