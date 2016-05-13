New BSD License

Copyright (c) 2007–2016 The scikit-learn developers.
All rights reserved.


Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

  a. Redistributions of source code must retain the above copyright notice,
     this list of conditions and the following disclaimer.
  b. Redistributions in binary form must reproduce the above copyright
     notice, this list of conditions and the following disclaimer in the
     documentation and/or other materials provided with the distribution.
  c. Neither the name of the Scikit-learn Developers  nor the names of
     its contributors may be used to endorse or promote products
     derived from this software without specific prior written
     permission. 


THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
ARE DISCLAIMED. IN NO EVENT SHALL THE REGENTS OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH
DAMAGE.

Copyright (c) 2016 Lakshay Piplani

This file is part of YourMessenger.

YourMessenger is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

YourMessenger is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with YourMessenger.  If not, see <http://www.gnu.org/licenses/>.

import pickle
import cPickle
import numpy
import string

from sklearn import cross_validation
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_selection import SelectPercentile, f_classif

vectorizer = TfidfVectorizer(sublinear_tf=True, max_df=0.5,
                                 stop_words='english')

selector = SelectPercentile(f_classif, percentile=10)

authors = []
word_data = []


def preprocess(words_file = "emails_long.pkl", authors_file="labels_long.pkl"):
    
    authors_file_handler = open(authors_file, "r")
    authors = pickle.load(authors_file_handler)
    authors_file_handler.close()

  
    
    words_file_handler = open(words_file, "r")
    word_data = cPickle.load(words_file_handler)
    words_file_handler.close()

    #print type(word_data)
    
    #print len(word_data)

    ### test_size is the percentage of events assigned to the test set
    ### (remainder go into training)
    features_train, features_test, labels_train, labels_test = cross_validation.train_test_split(word_data, authors, test_size=0.1, random_state=42)
    #print 'len of features_test', len(features_test)


    ### text vectorization--go from strings to lists of numbers
    #vectorizer = TfidfVectorizer(sublinear_tf=True, max_df=0.5,
    #                             stop_words='english')
    features_train_transformed = vectorizer.fit_transform(features_train)
    features_test_transformed  = vectorizer.transform(features_test)
    #print type(features_train_transformed[0]) --> sparse matrix
    """print type(features_test_transformed)
    print type(features_train_transformed)
    print features_train_transformed[0].toarray()[0,23503] --> ndarray
    he = vectorizer.get_feature_names() --> alphabetical order
    print he[len(he)/2 : len(he)/2 + 5]"""
    #print features_train_transformed[0]    
    #print features_train_transformed[0] -> sparse matrix
    #he = vectorizer.get_feature_names()
    
    
    selector.fit(features_train_transformed, labels_train)
    features_train_transformed = selector.transform(features_train_transformed).toarray()
    features_test_transformed  = selector.transform(features_test_transformed).toarray()

    """feat = selector.get_support(True)
    for f in feat[len(feat)/2: len(feat)/2 + 10]:
        print he[f], """


    #print type(features_train_transformed), numpy.shape(features_train_transformed)
    #print (features_train_transformed[0]), numpy.shape(features_train_transformed[0])

    ### info on the data
    print "no. of spam training emails:", sum(labels_train)
    print "no. of ham training emails:", len(labels_train)-sum(labels_train)
    
    return features_train_transformed, features_test_transformed, labels_train, labels_test



def predict(text):
    l = []
    l.append(text)

    textSparseVec = vectorizer.transform(l)
    textTrans = selector.transform(textSparseVec).toarray()

    return textTrans

def add(msg):

    threshFile = open("thresh.pkl", "r")
    threshDict = pickle.load(threshFile)
    threshFile.close()
    if msg in threshDict:
        threshDict[msg] += 1
    else:
        threshDict[msg] = 1

    

    if threshDict[msg] == 10:
        authors_file_handler = open("labels_long.pkl", "r")
        authors = pickle.load(authors_file_handler)
        authors_file_handler.close()

  
    
        words_file_handler = open("emails_long.pkl", "r")
        word_data = cPickle.load(words_file_handler)
        words_file_handler.close()
    

        words = msg.split()
        words_proc = [ word.strip(string.punctuation).lower() for word in words[1:] ]

        cnt = 0
        for x in words_proc:
            if x == "":
                cnt += 1
        for i in range(0, cnt):
            words_proc.remove('')
        text = string.join(words_proc)

        word_data.append(text)
        if words[0] == 'ham':
            authors.append(0)
        else:
            authors.append(1)

        f = open('emails_long.pkl', 'w')
        pickle.dump(word_data, f)
        f.close()

        f = open('labels_long.pkl', 'w')
        pickle.dump(authors, f)
        f.close()

        del threshDict[msg]
        threshFile = open("thresh.pkl", "w")
        pickle.dump(threshDict, threshFile)
        threshFile.close()

        return True

    else:
        threshFile = open("thresh.pkl", "w")
        pickle.dump(threshDict, threshFile)
        threshFile.close()
        return False










    


