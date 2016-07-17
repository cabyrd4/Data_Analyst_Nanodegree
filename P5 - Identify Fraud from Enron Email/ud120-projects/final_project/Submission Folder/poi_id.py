#!/usr/bin/python

import sys
import pickle
sys.path.append("../tools/")
from sklearn.preprocessing import MinMaxScaler
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.cross_validation import StratifiedShuffleSplit
from sklearn.ensemble import AdaBoostClassifier, RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
#from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.grid_search import GridSearchCV
from tester import test_classifier
from time import time
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

from feature_format import featureFormat, targetFeatureSplit
from tester import dump_classifier_and_data

### Task 1: Select what features you'll use.
### features_list is a list of strings, each of which is a feature name.
### The first feature must be "poi".
features_list = ['poi', 'salary', 'deferral_payments', 'total_payments', 
'loan_advances', 'bonus', 'restricted_stock_deferred', 'deferred_income', 
'total_stock_value', 'expenses', 'exercised_stock_options', 'other', 
'long_term_incentive', 'restricted_stock', 'director_fees', 'to_messages',
 #'email_address', 
 'from_poi_to_this_person', 'from_messages', 
'from_this_person_to_poi', 'shared_receipt_with_poi']

my_features_list = ['poi']

print "Features Count: ",len(features_list) - 1

### Load the dictionary containing the dataset
with open("final_project_dataset.pkl", "r") as data_file:
    data_dict = pickle.load(data_file)

### Task 1.2: Analyze & Preprocess Data
# Convert Dictionary into Panda's Dataframe
df = pd.DataFrame()
df = df.from_dict(data_dict, orient='index')
df.index.name = 'Name'
df.head()

# Delete "email_address" column
## It's not a quantative value to measure
df = df.drop(['email_address'], axis=1)

# Total Number of Data Points
print "Total Number of Data Points: ", df.count()

# Names of People in Dataset
df.index.values

# Allocation Across Classes
print "Total Number POIs: ", df['poi'].sum()
print "Total Number Non-POIs: ", df['poi'].count() - df['poi'].sum()

# Are There Features with Missing Values?
df = df.replace("NaN",np.nan)
missing_featres = df['poi'].count() - df.count()
print "Count of Missing Values by Feature: "
print missing_featres.sort_values(ascending=False)

# Are There Employees with Missing Values?
missing_employees = len(df.columns) - df.count(axis=1)
print "Count of Missing Values by Employees: "
print missing_employees.sort_values(ascending=False)

### Task 2: Remove outliers

# Graph to Show Outlier
df.plot.scatter(x='salary' , y='bonus')

# Query to Identify Outlier Name
outlier = df[df.salary > 10000000]
print outlier
    
# Actual Removal of Outliers    
df = df.drop(['LOCKHART EUGENE E', 'TOTAL', 'THE TRAVEL AGENCY IN THE PARK'])

# Updated Data Points Print Out
print "Total Number POIs: ", df['poi'].sum()
print "Total Number Non-POIs: ", df['poi'].count() - df['poi'].sum()

### Task 3: Create new feature(s)
# New Features to Measure Percentage of Email Correspondence with POI
## From POI
df["percentage_from_poi"] = df["from_poi_to_this_person"] / df["to_messages"]
#df.boxplot(column="percentage_from_poi",by='poi')

## To POI
df["percentage_to_poi"] = df["from_this_person_to_poi"] / df["from_messages"]
#df.boxplot(column="percentage_to_poi",by='poi')

# New Feature to Measure Total Compensation
df["total_compensation"] = df["total_payments"] + df["total_stock_value"]
#df.boxplot(column="total_compensation",by='poi')

# New Feature to Measure Retention Incentives
df["retention_incentives"] = df["long_term_incentive"] + df["total_stock_value"]
#df.boxplot(column="retention_incentives",by='poi')

# New Feature to Measure Salary Bonus Ratio
df["salary_bonus_ratio"] = df["bonus"] / df["salary"]
#df.boxplot(column="salary_bonus_ratio",by='poi')

### Organize Features List
my_features = list(df.columns.values)
my_features.remove('poi')
my_features = my_features_list + my_features
features_list = my_features

### Convert Dataframe back to Dictionary
df = df.fillna(0)
data_dict = df.to_dict('index')

### Store to my_dataset for easy export below.
my_dataset = data_dict

### Extract features and labels from dataset for local testing
data = featureFormat(my_dataset, features_list, sort_keys = True)
labels, features = targetFeatureSplit(data)

# Scale features
scaler = MinMaxScaler()
features = scaler.fit_transform(features)

## Stratifieldshufflesplit to find the best subset of features to use
print "Selecting Feautres: "
scv = StratifiedShuffleSplit(labels, 1000, random_state = 42)

# Decision Tree
DT_acc = []	
DT_precision = []
DT_recall = []

# AdaBoost Classifier
ADA_acc = []	
ADA_precision = []
ADA_recall = []

# Random Forest
RF_acc = []
RF_precision = []
RF_recall = []

# K-Nearest Neighbors
KNN_acc = []
KNN_precision = []
KNN_recall = []

### Task 4: Try a varity of classifiers
### Please name your classifier clf for easy export below.
### Note that if you want to do PCA or other multi-stage operations,
### you'll need to use Pipelines. For more info:
### http://scikit-learn.org/stable/modules/pipeline.html

# Function to help train and test classifiers using Cross-Validation
def cvClassifier(clf, features, labels, cv):
    true_negatives = 0
    false_negatives = 0
    true_positives = 0
    false_positives = 0
    for train_idx, test_idx in cv: 
        features_train = []
        features_test  = []
        labels_train   = []
        labels_test    = []
        for ii in train_idx:
            features_train.append( features[ii] )
            labels_train.append( labels[ii] )
        for jj in test_idx:
            features_test.append( features[jj] )
            labels_test.append( labels[jj] )
        clf.fit(features_train, labels_train)
        predictions = clf.predict(features_test)
        for prediction, truth in zip(predictions, labels_test):
            if prediction == 0 and truth == 0:
                true_negatives += 1
            elif prediction == 0 and truth == 1:
                false_negatives += 1
            elif prediction == 1 and truth == 0:
                false_positives += 1
            elif prediction == 1 and truth == 1:
                true_positives += 1
    total_predictions = true_negatives + false_negatives + false_positives + true_positives
    accuracy = round(1.0*(true_positives + true_negatives)/total_predictions,2)
    if true_positives+false_positives == 0:
        precision = 0
    else:
        precision = round(1.0*true_positives/(true_positives+false_positives),2)
    if true_positives+false_negatives == 0:
        recall = 0
    else:
        recall = round(1.0*true_positives/(true_positives+false_negatives),2)
    return accuracy, precision, recall

# Train Classifers for each of the Best-K Features
for i in range(len(features[0])):
    t0 = time()
    selector = SelectKBest(f_classif, k = i+1)
    selector.fit(features, labels)
    reduced_features = selector.fit_transform(features, labels)
    cutoff = np.sort(selector.scores_)[::-1][i]
    selected_features_list = [f for j, f in enumerate(features_list[1:]) if selector.scores_[j] >= cutoff]
    selected_features_list = ['poi'] + selected_features_list
    
    # Stated Classifers    
    DT = DecisionTreeClassifier(random_state=123)    
    ADA = AdaBoostClassifier(random_state=123)
   # GNB = GaussianNB()
    RF = RandomForestClassifier(random_state=123)
    KNN = KNeighborsClassifier()
    
    # Decision Tree    
    acc, precision, recall = cvClassifier(DT, reduced_features, labels, scv)
    DT_acc.append(acc)
    DT_precision.append(precision)
    DT_recall.append(recall)
    
    # AdaBoost    
    acc, precision, recall = cvClassifier(ADA, reduced_features, labels, scv)
    ADA_acc.append(acc)
    ADA_precision.append(precision)
    ADA_recall.append(recall)

    # Random Forest
    acc, precision, recall = cvClassifier(RF, reduced_features, labels, scv)
    RF_acc.append(acc)
    RF_precision.append(precision)
    RF_recall.append(recall)
    
    # K-Nearest Neighbor   
    acc, precision, recall = cvClassifier(KNN, reduced_features, labels, scv)
    KNN_acc.append(acc)
    KNN_precision.append(precision)
    KNN_recall.append(recall) 
    
    # Time Recording    
    print "fitting time in seconds for k = {0}: {1}".format(i+1, round(time()-t0, 3))
    
    # Print Out Score, Precision, and Recall by Classifier and K Feature    
    print "DT accuracy: {0}  precision: {1}  recall: {2}".format(DT_acc[-1], DT_precision[-1], DT_recall[-1])
    print "ADA accuracy: {0}  precision: {1}  recall: {2}".format(ADA_acc[-1], ADA_precision[-1], ADA_recall[-1])
    print "RF accuracy: {0}  precision: {1}  recall: {2}".format(RF_acc[-1], RF_precision[-1], RF_recall[-1])
    print "KNN accuracy: {0}  precision: {1}  recall: {2}".format(KNN_acc[-1], KNN_precision[-1], KNN_recall[-1])

# Create Dataframes of results to graph
dt_df = pd.DataFrame({'DT_pre': DT_precision, 'DT_rec': DT_recall})
ada_df = pd.DataFrame({'ADA_pre': ADA_precision, 'ADA_rec': ADA_recall}) 
rf_df = pd.DataFrame({'RF_pre': RF_precision, 'RF_rec': RF_recall})
knn_df = pd.DataFrame({'KNN_pre': KNN_precision, 'KNN_rec': KNN_recall})                  

# Graphs
dt_df.plot()
plt.show()

ada_df.plot()
plt.show()

rf_df.plot()
plt.show()

knn_df.plot()
plt.show()

print "------" 
# Decision Tree Features & Importance
print "Decision Tree Features & Importance"
selector = SelectKBest(f_classif, k = DT_recall.index(max(DT_recall))+1)
selector.fit(features, labels)
cutoff = np.sort(selector.scores_)[::-1][DT_recall.index(max(DT_recall))+1]
selected_features_list = [f for i, f in enumerate(features_list[1:]) if selector.scores_[i] > cutoff]
selected_features_list = ['poi'] + selected_features_list
selected_features = selector.fit_transform(features, labels)

print "Number of Features Selected: ", len(selected_features_list)-1
print "Featues Selected: "
for f in selected_features_list[1:]:
    print f

DT = DecisionTreeClassifier(random_state=123)
DT.fit(selected_features, labels)
print "Feature Importance for the Selected Features: "
print DT.feature_importances_

print "Feature Scores for the Selected Features from SelectKBest: "
for f in selected_features_list[1:]:
	print f, "score is: ", selector.scores_[features_list[1:].index(f)]
print "------"
 
# AdaBoost Features & Importance
print "AdaBoost Features & Importance"
selector = SelectKBest(f_classif, k = ADA_recall.index(max(ADA_recall))+1)
selector.fit(features, labels)
cutoff = np.sort(selector.scores_)[::-1][ADA_recall.index(max(ADA_recall))+1]
selected_features_list = [f for i, f in enumerate(features_list[1:]) if selector.scores_[i] > cutoff]
selected_features_list = ['poi'] + selected_features_list
selected_features = selector.fit_transform(features, labels)

print "Number of Features Selected: ", len(selected_features_list)-1
print "Featues Selected: "
for f in selected_features_list[1:]:
    print f

ADA = AdaBoostClassifier(random_state=123)
ADA.fit(selected_features, labels)
print "Feature Importance for the Selected Features: "
print ADA.feature_importances_

print "Feature Scores for the Selected Features from SelectKBest: "
for f in selected_features_list[1:]:
	print f, "score is: ", selector.scores_[features_list[1:].index(f)]
print "------" 

# Random Forest Features & Importance
print "Random Forrest Features & Importance"
selector = SelectKBest(f_classif, k = RF_recall.index(max(RF_recall))+1)
selector.fit(features, labels)
cutoff = np.sort(selector.scores_)[::-1][RF_recall.index(max(RF_recall))+1]
selected_features_list = [f for i, f in enumerate(features_list[1:]) if selector.scores_[i] > cutoff]
selected_features_list = ['poi'] + selected_features_list
selected_features = selector.fit_transform(features, labels)

print "Number of Features Selected: ", len(selected_features_list)-1
print "Featues Selected: "
for f in selected_features_list[1:]:
    print f

RF = RandomForestClassifier(random_state=123)
RF.fit(selected_features, labels)
print "Feature Importance for the Selected Features: "
print RF.feature_importances_

print "Feature Scores for the Selected Features from SelectKBest: "
for f in selected_features_list[1:]:
	print f, "score is: ", selector.scores_[features_list[1:].index(f)]
print "------"
 
# K-Nearest Neighbor Features & Importance
print "K-Nearest Neighbor Features & Importance"
selector = SelectKBest(f_classif, k = KNN_recall.index(max(KNN_recall))+1)
selector.fit(features, labels)
cutoff = np.sort(selector.scores_)[::-1][KNN_recall.index(max(KNN_recall))+1]
selected_features_list = [f for i, f in enumerate(features_list[1:]) if selector.scores_[i] > cutoff]
selected_features_list = ['poi'] + selected_features_list
selected_features = selector.fit_transform(features, labels)

print "Number of Features Selected: ", len(selected_features_list)-1
print "Featues Selected: "
for f in selected_features_list[1:]:
    print f

KNN = KNeighborsClassifier()
KNN.fit(selected_features, labels)
#print "Feature Importance for the Selected Features: "
#print KNN.feature_importances_

print "Feature Scores for the Selected Features from SelectKBest: "
for f in selected_features_list[1:]:
	print f, "score is: ", selector.scores_[features_list[1:].index(f)]
print "------"

### Task 5: Tune your classifier to achieve better than .3 precision and recall 
### using our testing script. Check the tester.py script in the final project
### folder for details on the evaluation method, especially the test_classifier
### function. Because of the small size of the dataset, the script uses
### stratified shuffle split cross validation. For more info: 
### http://scikit-learn.org/stable/modules/generated/sklearn.cross_validation.StratifiedShuffleSplit.html

# Tuning Decison Tree
print "Tuning Decision Tree"
t0 = time()
tuning_parameters = {'criterion': ['gini', 'entropy'],
         'min_samples_split': [2, 6, 8, 10, 15, 20, 30],
          'max_depth': [2, 6, 8, 10, 15, 20, 30]}
print("Tuning Parameters for Recall")
DT = GridSearchCV(DecisionTreeClassifier(), tuning_parameters, cv=scv, scoring = 'recall')
DT.fit(selected_features, labels)
print("Best parameters are:")
print(DT.best_params_)
print "tunning time: {0}".format(round(time()-t0, 3))

Clf = DT.best_estimator_
print "measurements for tuned random forest classifier: "
test_classifier(Clf, my_dataset, selected_features_list, folds = 1000)
print "------"

# Tuning AdaBoost
print "Tuning AdaBoost"
t0 = time()
tuning_parameters = {'n_estimators': [10,25,50,100,200], 
              'learning_rate': [0.2,0.4,0.6,0.8,1]}
print("Tuning Parameters for Recall")
ADA = GridSearchCV(AdaBoostClassifier(), tuning_parameters, cv=scv, scoring = 'recall')
ADA.fit(selected_features, labels)
print("Best parameters are:")
print(ADA.best_params_)
print "tunning time: {0}".format(round(time()-t0, 3))

Clf = ADA.best_estimator_
print "measurements for tuned random forest classifier: "
test_classifier(Clf, my_dataset, selected_features_list, folds = 1000)
print "------"

# Tuning Random Forest
print "Tuning Random Forest"
t0 = time()
tuning_parameters = {'n_estimators': [20,50,100], 
              'min_samples_split': [1,2,4], 
              'max_features': [1,2,3]}
print("Tuning Parameters for Recall")
RF = GridSearchCV(RandomForestClassifier(), tuning_parameters, cv=scv, scoring = 'recall')
RF.fit(selected_features, labels)
print("Best parameters are:")
print(RF.best_params_)
print "tunning time: {0}".format(round(time()-t0, 3))

Clf = RF.best_estimator_
print "measurements for tuned random forest classifier: "
test_classifier(Clf, my_dataset, selected_features_list, folds = 1000)
print "------"

# Tuning K-Nearest Neighbors
print "Tuning K-Nearest Neighbors"
t0 = time()
tuning_parameters = {'n_neighbors': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
              'weights': ('uniform', 'distance'),
                'algorithm': ('auto', 'ball_tree', 'kd_tree', 'brute'),
                'leaf_size': [1, 5, 10, 20, 30, 40, 50, 75, 100, 200]}
print("Tuning Parameters for Recall")
KNN = GridSearchCV(KNeighborsClassifier(), tuning_parameters, cv=scv, scoring = 'recall')
KNN.fit(selected_features, labels)
print("Best parameters are:")
print(KNN.best_params_)
print "tunning time: {0}".format(round(time()-t0, 3))

Clf = KNN.best_estimator_
print "measurements for tuned random forest classifier: "
test_classifier(Clf, my_dataset, selected_features_list, folds = 1000)

## Final Selection and Evaluation
clf = RF.best_estimator_

### Task 6: Dump your classifier, dataset, and features_list so anyone can
### check your results. You do not need to change anything below, but make sure
### that the version of poi_id.py that you submit can be run on its own and
### generates the necessary .pkl files for validating your results.

dump_classifier_and_data(clf, my_dataset, selected_features_list)