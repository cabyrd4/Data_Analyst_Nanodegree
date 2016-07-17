#!/usr/bin/python

""" 
    This is the code to accompany the Lesson 2 (SVM) mini-project.

    Use a SVM to identify emails from the Enron corpus by their authors:    
    Sara has label 0
    Chris has label 1
"""
    
import sys
from time import time
sys.path.append("../tools/")
from email_preprocess import preprocess


### features_train and features_test are the features for the training
### and testing datasets, respectively
### labels_train and labels_test are the corresponding item labels
t0 = time()
features_train, features_test, labels_train, labels_test = preprocess()
print "preprocessing time:", round(time()-t0, 3), "s"



#########################################################
### your code goes here ###
from sklearn.svm import SVC
t0 = time()
clf = SVC(kernel="rbf", C=10000.0)

#features_train = features_train[:len(features_train)/100] 
#labels_train = labels_train[:len(labels_train)/100] 

clf.fit(features_train, labels_train)
print "training time:", round(time()-t0, 3), "s"

t0 = time()
pred = clf.predict(features_test)
print "prediction time:", round(time()-t0, 3), "s"

from sklearn.metrics import accuracy_score
acc = accuracy_score(pred, labels_test)

print "The accuracy on the test set is: ",acc
print "The 10th is predicted to be ",pred[10]
print "The 26th is predicted to be ",pred[26]
print "The 50th is predicted to be ",pred[50]

s = 0
for p in pred:
	if p == 1:
		s += 1

print s
#########################################################


