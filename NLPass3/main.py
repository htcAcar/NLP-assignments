
from gensim.models import KeyedVectors
import operator
import numpy as np
import scipy.spatial.distance as distance
from np.magic import np

from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn import utils
import csv
from tqdm import tqdm
import nltk


tqdm.pandas(desc="progress-bar")
filename = 'GoogleNews-vectors-negative300.bin'

model1 = KeyedVectors.load_word2vec_format(filename, binary=True,limit=5000)

lc=0
lc2=0
count=0
vocabulary = model1.vocab

def tokenize_text(text):
    tokens = []
    for line in nltk.sent_tokenize(text):
        for word in nltk.word_tokenize(line):
            tokens.append(word.lower())
    return tokens

def vector_for_learning(model, input_docs):
    sents = input_docs
    targets, feature_vectors = zip(*[(doc.tags[0], model.infer_vector(doc.words, steps=20)) for doc in sents])
    return targets, feature_vectors

def cosine(vec):
    result = {}
    for key in vocabulary.keys():
        a = np.array(vec)
        b = np.array(model1.wv[key])
        c = 1 - distance.cosine(a, b)
        result[key] = c
        print(key,c)
    guess = max(result.items(), key=operator.itemgetter(1))[0]
    return  guess

with open("word-test.v1.txt", "r") as f:
    for line in f:
        lc+=1
        word = line.rstrip("\n").split()
        # print(line,count,word[0])
        if(lc>1 and word[0]!=":"):
            if((word[0] in model1.wv)and (word[1] in model1.wv) and (word[2] in model1.wv)and (word[3] in model1.wv)):
                v1 = model1.wv[word[0]]
                v2 = model1.wv[word[1]]
                v3 = model1.wv[word[2]]
                v4 = model1.wv[word[3]]
                lc2+=1
                vec=v2-v1+v3

                guess=cosine(vec)
                if (guess == word[3]):
                  count+=1


accuracy=count/lc2
print("Accuracy : ",accuracy)

# # -----------------------------------------TASK2------------------------------------------
# train_data= []
# test_data= []
#
# film_type = {'sci-fi': 1 , 'action': 2, 'comedy': 3, 'fantasy': 4, 'animation': 5, 'romance': 6}
#
# linec=0
#
# with open('tagged_plots_movielens.csv', 'r') as csvfile:
#     data = csv.reader(csvfile, delimiter=',', quotechar='"')
#     for line in data:
#         linec+=1
#         if (linec <= 2000):
#             train_data.append(TaggedDocument(words=tokenize_text(line[2]), tags=[film_type.get(line[3],6)] ))
#
#         else:
#             test_data.append( TaggedDocument(words=tokenize_text(line[2]),
#     tags=[film_type.get(line[3],6)]))
#
#
#
# model_doc2vec=Doc2Vec(dm=1, vector_size=300, negative=5,  min_count=2, sample = 0,  alpha=0.025, min_alpha=0.001)
# model_doc2vec.build_vocab([x for x in tqdm(train_data)])
#
# train_data  = utils.shuffle(train_data)
# model_doc2vec.train(train_data,total_examples=len(train_data), epochs=10)
#
#
# y_train, x_train = vector_for_learning(model_doc2vec, train_data)
# y_test, x_test = vector_for_learning(model_doc2vec, test_data)
#
# logreg = LogisticRegression()
# logreg.fit(x_train, y_train)
# y_predict = logreg.predict(x_test)
#
# print("Accuracy : " ,accuracy_score(y_test, y_predict))

