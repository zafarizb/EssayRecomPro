# -*- coding: utf-8 -*-
from nltk.tokenize import word_tokenize
import jieba
import os
###### This is for a series of passages

def Preprocess_Essays(argv):
    # Preprocess1-1: Tokenize--English
    # English tokenized
    texts_tokenized_0 = [[word.lower() for word in word_tokenize(document)] for document in argv] # This is for several documents
    texts_tokenized = []
    # Preprocess1-2: Tokenize--Chinese
    for i in texts_tokenized_0:
        li = []
        for j in i:
            s = j.strip()
            word = jieba.cut(s, cut_all=False)
            for k in word:
                li.append(k)
        texts_tokenized.append(li)

    # Preprocess2-1: Delete stopwords--English
    from nltk.corpus import stopwords
    english_stopwords = stopwords.words('english')
    texts_filtered_stopwords_1 = [[word for word in document if not word in english_stopwords] for document in
                            texts_tokenized]
    # Preprocess2-2: Delete stopwords--Chinese
    cn_stpwrdpath = "stop_words_cn.txt"
    cn_stpwrd_dic = open(os.path.join("/home/lsl/InitData",cn_stpwrdpath), encoding='gbk')
    cn_stpwrd_content = cn_stpwrd_dic.read()
    # 将停用词表转换为list
    chinese_stopwords = cn_stpwrd_content.splitlines()
    cn_stpwrd_dic.close()
    texts_filtered_stopwords_2 = [[word for word in document if not word in chinese_stopwords] for document in
                                  texts_filtered_stopwords_1]


    # Preprocess3: Try to delete the punctuations
    punctuations = [',', '.', ':', ';', '?', '(', ')', '[', ']', '&', '!', '*', '@', '#', '$', '%','。','，',
                            '：', '；', '？', '（', '）', '【', '】', '&', '！', '*', '@', '#', '￥', '%','、']
    texts_filtered = [[word for word in document if not word in punctuations] for document in
                      texts_filtered_stopwords_2]

    # Preprocess4: Stemming
    from nltk.stem.lancaster import LancasterStemmer

    st = LancasterStemmer()
    texts_stemmed = [[st.stem(word) for word in document] for document in texts_filtered]

    return texts_stemmed

    # To increase the speed
    '''
    # Preprocess5; Delete words that only appear once
    all_stems = sum(texts_stemmed, [])
    stems_once = set(stem for stem in set(all_stems) if all_stems.count(stem) == 1)


    texts = [[stem for stem in text if stem not in stems_once] for text in texts_stemmed]
    return texts
    '''
if __name__ == '__main__':
    f_essay1 = open("./dataset/essay1.txt",encoding='utf-8')
    essay1 = f_essay1.read()
    f_essay2 = open("./dataset/essay2.txt",encoding='utf-8')
    essay2 = f_essay2.read()
    Preprocess_Essays([essay1,essay2])