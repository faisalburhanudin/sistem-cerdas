import json
import os

import numpy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.svm import LinearSVC

current_dir = os.path.join(os.path.dirname(__file__), 'dataset')


def create_tfidf():
    return TfidfVectorizer(analyzer='word', binary=False, decode_error='ignore',
                           dtype=numpy.int64, encoding='utf-8', input='content',
                           lowercase=True, max_df=1.0, max_features=None, min_df=1,
                           ngram_range=(1, 1), norm='l2', preprocessor=None, smooth_idf=True,
                           stop_words=None, strip_accents=None, sublinear_tf=False,
                           token_pattern='(?u)\\b\\w\\w+\\b', tokenizer=None, use_idf=True,
                           vocabulary=None)


def create_clf():
    return LinearSVC(C=1.0, class_weight=None, dual=True, fit_intercept=True,
                     intercept_scaling=1, loss='squared_hinge', max_iter=1000,
                     multi_class='ovr', penalty='l2', random_state=None, tol=0.0001,
                     verbose=0)


def load_data():
    with open(os.path.join(current_dir, 'spam.json')) as f:
        spam_json = json.load(f)

    with open(os.path.join(current_dir, 'not_spam.json')) as f:
        not_spam_json = json.load(f)

    label_spam = numpy.full((len(spam_json),), 0)
    label_not_spam = numpy.full((len(not_spam_json),), 1)

    data = spam_json + not_spam_json
    label = numpy.concatenate((label_spam, label_not_spam))
    return data, label


if __name__ == '__main__':
    x, y = load_data()
    X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42, stratify=y)

    tfidf = create_tfidf()
    x_transform = tfidf.fit_transform(X_train)

    clf = create_clf()
    clf.fit(x_transform, y_train)

    x_test_transform = tfidf.transform(X_test)
    y_pred = clf.predict(x_test_transform)

    acc = accuracy_score(y_test, y_pred)
    print(acc)
