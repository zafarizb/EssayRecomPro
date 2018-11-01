# -*- coding: utf-8 -*-
#import logging
#logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
from gensim import corpora, models, similarities
from nltk.tokenize import word_tokenize
#import  NLTK_essays
from . import  NLTK_essays
from . import  NLTK_handin
import codecs
##################### This is to calculate the similarity between 1 essays and other essays

# 中文注释
# Read the text
# If the texts are stored in different .txt
'''courses = [line.strip() for line in file('coursera_corpus')]
courses_name = [course.split('\t')[0] for course in courses] # The structure is coursename\tcourse intro\tcourse detail
print courses_name[0:10]
'''

# Input：Texts from one teacher. A text from a student.
# Output: The average similarity between this teacher's essays and the student's essays
# argv: handin filename; teacher's filename1; teacher's filename2
def Similarity(studentessay,teacheressays):
    print('similarity1')
    handin = studentessay
    essays = []
    for i in teacheressays:
        essays.append(i)

    # Preprocess of the text
    texts = essays
        #texts = NLTK_essays.Preprocess_Essays(essays)
    print('similarity2')
    print(len(texts))

    # Use gensim
    # Dictionarize
    dictionary = corpora.Dictionary(texts)
    corpus = [dictionary.doc2bow(text) for text in texts]



    # Tf-idf Model
    tfidf = models.TfidfModel(corpus)
    corpus_tfidf = tfidf[corpus]

    print('similarity3')
    # Set and train the LSI model
    lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=200)

    # The index matrix to store the lsi model of each topic. # The size of matrix here is 2 documents * 10 features
    index = similarities.MatrixSimilarity(lsi[corpus])


    # The essay handed in by the student
    ml_handin = handin
    #ml_handin = NLTK_handin.Preprocess_Handin(handin)
    ml_bow = dictionary.doc2bow(ml_handin)
    ml_lsi = lsi[ml_bow]

    print('similarity4')
    sims = index[ml_lsi]  # Compare the lsi model of student's essay to the teacher's essay
    sort_sims = sorted(enumerate(sims), key=lambda item: -item[1])
    #print(sort_sims) # Form: (num, similarity)
    return sort_sims

#if __name__ == '__main__':
    #Similarity(["./dataset/cloud.txt","./dataset/nn.txt","./dataset/sdn.txt"])