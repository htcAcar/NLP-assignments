
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn import utils
import csv
from tqdm import tqdm
import nltk


tqdm.pandas(desc="progress-bar")

def tokenize_text(text):
    tokens = []
    for line in nltk.sent_tokenize(text):
        for word in nltk.word_tokenize(line):
            tokens.append(word.lower())
    return tokens


train_data= []
test_data= []

film_type = {'sci-fi': 1 , 'action': 2, 'comedy': 3, 'fantasy': 4, 'animation': 5, 'romance': 6}


lc=0

with open('tagged_plots_movielens.csv', 'r') as csvfile:
    data = csv.reader(csvfile, delimiter=',', quotechar='"')
    for line in data:
        lc+=1
        if (lc <= 2000):
            train_data.append(TaggedDocument(words=tokenize_text(line[2]), tags=[film_type.get(line[3],6)] ))

        else:
            test_data.append( TaggedDocument(words=tokenize_text(line[2]),
    tags=[film_type.get(line[3],6)]))

print(train_data[0])



model_doc2vec=Doc2Vec(dm=1, vector_size=300, negative=5,  min_count=2, sample = 0,  alpha=0.025, min_alpha=0.001)
model_doc2vec.build_vocab([x for x in tqdm(train_data)])

train_data  = utils.shuffle(train_data)
model_doc2vec.train(train_data,total_examples=len(train_data), epochs=10)

def vector_for_learning(model, input_docs):
    sents = input_docs
    targets, feature_vectors = zip(*[(doc.tags[0], model.infer_vector(doc.words, steps=20)) for doc in sents])
    return targets, feature_vectors


y_train, x_train = vector_for_learning(model_doc2vec, train_data)
y_test, x_test = vector_for_learning(model_doc2vec, test_data)

logreg = LogisticRegression()
logreg.fit(x_train, y_train)
y_predict = logreg.predict(x_test)

print("Accuracy : " ,accuracy_score(y_test, y_predict))


































# import pandas as pd
# from sklearn.model_selection import train_test_split
# data = pd.read_csv("tagged_plots_movielens.csv",error_bad_lines=False)
# print(data.head())
#
# y = data.tag
# X = data.drop('tag;;;;;;;;;', axis=1)
#
# X_train, X_test, y_train, y_test = train_test_split(X, y,test_size=0.2)
# print("\nX_train:\n")
# print(X_train.head())
# print(X_train.shape)
#
# print("\nX_test:\n")
# print(X_test.head())
# print(X_test.shape)


# import numpy as np
# import pandas as pd
#
# def train_validate_test_split(df, train_percent=.6, validate_percent=.2, seed=None):
#     np.random.seed(seed)
#     perm = np.random.permutation(df.index)
#     m = len(df.index)
#     train_end = int(train_percent * m)
#     train = df.ix[perm[:train_end]]
#     test = df.ix[perm[train_end:]]
#     return train, test
# np.random.seed([3,1415])
# df = pd.DataFrame(np.random.rand(10, 5), columns=list('ABCDE'))
# print(df)
# train, validate, test = train_validate_test_split(df)
# import pandas as pd
# import numpy as np
# from tqdm import tqdm
# tqdm.pandas(desc="progress-bar")
# from gensim.models import Doc2Vec
# from sklearn import utils
# from sklearn.model_selection import train_test_split
# import gensim
# from sklearn.linear_model import LogisticRegression
# from gensim.models.doc2vec import TaggedDocument
# import re
# import seaborn as sns
# import matplotlib.pyplot as plt
#
# df = pd.read_csv('Consumer_Complaints.csv',error_bad_lines=False,low_memory=False)
# df = df[['Consumer complaint narrative','Product']]
# df = df[pd.notnull(df['Consumer complaint narrative'])]
# df.rename(columns = {'Consumer complaint narrative':'narrative'}, inplace = True)
# df.head(10)
# df.shape
# df.index = range(37211)
#
# df['narrative'].apply(lambda x: len(x.split(' '))).sum()
# cnt_pro = df['Product'].value_counts()
#
# plt.figure(figsize=(12,4))
# sns.barplot(cnt_pro.index, cnt_pro.values, alpha=0.8)
# plt.ylabel('Number of Occurrences', fontsize=12)
# plt.xlabel('Product', fontsize=12)
# plt.xticks(rotation=90)
# plt.show();