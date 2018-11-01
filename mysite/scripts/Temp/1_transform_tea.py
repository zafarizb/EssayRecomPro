from recomm.models import Teacher,Student,TeacherEssay,StudentEssay,Relation
from recomm.tools.pdf2txt import PdfTranstorm
from recomm.tools.NLTK_handin import Preprocess_Handin
import pandas as pd
import os
import pdfminer
import codecs
#import slate
from pandas import DataFrame

def run():
    # init teachers' essays
    not_found = []
    type_error = []
    print('Transforming teacher essays from pdf to txt...')
    teacheressays = pd.read_csv(os.path.join("/home/lsl/InitData/new_data", "add_teacheressay.csv"), sep=',', encoding='utf_8_sig')
    for i in range(len(teacheressays['论文题目'])):
        if isinstance(teacheressays.iloc[i, 2], str):  # 有论文的项才处理
            id = teacheressays.iloc[i, 0]
            sname = teacheressays.iloc[i, 1]
            name = sname.strip()
            stitle = teacheressays.iloc[i, 2]
            title = stitle.strip()
            # read the essay
        try:
            PdfTranstorm(['-o', os.path.join("/home/lsl/InitData\TeacherEssay", name, title + '.txt'), '-t', 'text',
                          os.path.join("/home/lsl/InitData\TeacherEssay", name, title + '.pdf')])
        except FileNotFoundError:
            print('not found error')
            print(name)
            print(title)
            not_found.append({name:title})
        except pdfminer.pdfparser.PDFSyntaxError:
            print('type error')
            print(name)
            print(title)
            type_error.append({name:title})
        except pdfminer.pdfdocument.PDFTextExtractionNotAllowed:
            print('type error')
            print(name)
            print(title)
            type_error.append({name:title})
        except KeyError:
            print('type error')
            print(name)
            print(title)
            type_error.append({name:title})
        else:
            print(name)
            print(title)
    print('not found:')
    for i in range(len(not_found)):
        print(not_found[i])
    print('type error:')
    for i in range(len(type_error)):
        print(type_error[i])