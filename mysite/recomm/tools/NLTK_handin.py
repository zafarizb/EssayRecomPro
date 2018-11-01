# -*- coding: utf-8 -*-
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import jieba
import os
###This is for a single passage

def Preprocess_Handin(argv):
    # Preprocess1-1: Tokenize--English
    # texts_tokenized = [[word.lower() for word in word_tokenize(document.decode('utf-8'))] for document in courses]
    ######### decode() is the method for string
    texts_tokenized_0 = [word.lower() for word in word_tokenize(argv)] # This is for several documents
    # Preprocess1-2: Tokenize--Chinese
    texts_tokenized = []
    for i in range(len(texts_tokenized_0)):
        item = texts_tokenized_0[i]
        s = item.strip()
        text = jieba.cut(s, cut_all=False) # Chinese tokenized
        for i in text:
            texts_tokenized.append(i)

    # Preprocess2-1: Delete stopwords--English stopword
    english_stopwords = stopwords.words('english')
    texts_filtered_stopwords_1 = [word for word in texts_tokenized if not word in english_stopwords] # Chinese stopwords
    # Preprocess2-2: Delete stopwords--Chinese stopword
    cn_stpwrdpath = "stop_words_cn.txt"
    cn_stpwrd_dic = open(os.path.join("/home/lsl/InitData",cn_stpwrdpath), encoding='gbk')
    cn_stpwrd_content = cn_stpwrd_dic.read()
    # 将停用词表转换为list
    chinese_stopwords = cn_stpwrd_content.splitlines()
    cn_stpwrd_dic.close()
    texts_filtered_stopwords_2 = [word for word in texts_filtered_stopwords_1 if not word in chinese_stopwords]

    # Try to delete the punctuations
    punctuations = [',', '.', ':', ';', '?', '(', ')', '[', ']', '&', '!', '*', '@', '#', '$', '%','。','，',
                            '：', '；', '？', '（', '）', '【', '】', '&', '！', '*', '@', '#', '￥', '%','、']
    texts_filtered = [word for word in texts_filtered_stopwords_2 if not word in punctuations]


    # Preprocess3: Stemming
    from nltk.stem.lancaster import LancasterStemmer

    st = LancasterStemmer()
    texts_stemmed = [st.stem(word) for word in texts_filtered]

    # Preprocess4; Delete words that only appear once
    all_stems = texts_stemmed
    stems_once = set(stem for stem in set(all_stems) if all_stems.count(stem) == 1)
    texts = [stem for stem in texts_stemmed if stem not in stems_once]

    return texts

if __name__ == '__main__':
    f_handin = open("./dataset/essay1.txt",encoding='utf-8')
    handin = f_handin.read()
    Preprocess_Handin(handin)