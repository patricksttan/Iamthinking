"""
Kaggle.com HDP
"""


"""
firstly convert the text into vector space, because SVM can only deal with numeric value
"""

# tried with a small set of the dataset
# here should use pandas to read...
import csv
with open('/Users/apple/Desktop/HDP/train.csv', 'rU') as f:
    f_csv = csv.reader(f)
    column = [row[3] for row in f_csv]

t1000 = column

# print t1000
# #think how to deal with the "multiply" and "in." and "()" inside the text

from sklearn.feature_extraction.text import CountVectorizer
vectorizer = CountVectorizer()

vectorizer.fit_transform(t1000)
print "Vocabulary:", vectorizer.vocabulary

# # #train_x =  # training data

# seems wrong
train_y =  t1000[3]

train_x = vectorizer.transform(t1000)
train_x.todense()

train_x = vectorizer.transform(t1000)
train_x.todense()

from sklearn.feature_extraction.text import TfidfTransformer
tfidf = TfidfTransformer(norm="l2")
tfidf.fit(train_x)

tfidf_train_x = tfidf.transform(train_x)



"""
finally, we should get the train_x(two values) with many dims and train_y(just the relevance)

The next step is classification into different categories to get w and t
"""
from sklearn import svm
clf = svm.SVR()
clf.fit(tfidf_train_x, train_y)
# refer to Trial2
# refer to svm

"""
In each category, do the regression(linear regression? Tree-based regression?) get the coefficient
"""

# refer to MLiA ch.8 ch.9