# -*- coding: utf-8 -*-

#takes 'matchedExamples-100-400-complete.csv' as input.
#training a Logistic Regression classifier using the curated training/test data and the computed feature vector
#evaluates the performance of the classifier on: accuracy, f1 score, precision-recall AUC
#also computes and outputs the feature importances of each feature.
#outputs graphs on: precision-recall ROC and feature importances
#additional code for hyperparameter tuning and feature importance is included (commented out)

import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix ,accuracy_score, f1_score, roc_curve, auc,precision_recall_curve
from sklearn.preprocessing import OneHotEncoder,StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.decomposition import TruncatedSVD
from sklearn.model_selection import RandomizedSearchCV
import numpy as np

print("TRAINING LOGISTIC REGRESSION MODEL")
conferenceNames=pd.read_csv('matchedExamples-100-400-complete.csv')
conferenceNames.head()

#define the target y and input values X
y = conferenceNames.pop('correct_match').values
X = conferenceNames.values

onehot_encoder = OneHotEncoder(sparse=False)
oheX = onehot_encoder.fit_transform(X)

#FEATURE IMPORTANCE 1:
#create a dataframe for the feature vector from the input values (remove input strings)
#columns=["researcher_name","obrss_name","publication_channel","best_match_score","fuzz_ratio","fuzz_partial_ratio","fuzz_token_sort_ratio","kmpMatch","BM_badCharMatch","rabinKarpMatch"]
#index = [f'{num}' for num in range(541)]
#X_dataframe=pd.DataFrame(X, columns=columns, index=index)
#X_featureVector=X_dataframe.drop(['researcher_name'], axis = 1)
#X_featureVector=X_featureVector.drop(['obrss_name'], axis = 1)
#
#store the publication channel feature values separately and apply one hot encoding to them
#publication_channel = X_featureVector['publication_channel']
#publication_channel=publication_channel.values.reshape(-1,1)
#
# One Hot Encoding
#onehot_encoder = OneHotEncoder(sparse=False)
#ohePubChannel = onehot_encoder.fit_transform(publication_channel)
#
#create a dataframe of the one hot encoded publication channel values. 
#each column in the dataframe respresents a category.
#columns=[f'{num}' for num in range(4)]
#index = [f'{num}' for num in range(541)]
#pubChanOHE=pd.DataFrame(ohePubChannel, columns=columns, index=index)
#pubChanOHE=pubChanOHE.astype(int)
#isConference = pubChanOHE["0"]
#isOther= pubChanOHE["1"]
#isJournal =pubChanOHE["2"]
#isWorkshop= pubChanOHE["3"]
#
#merge the individual publication channels back into the feature vector. 
#remove the publication channel column and convert to float
#X_featureVector["isConference"]=isConference
#X_featureVector["isOther"]=isOther
#X_featureVector["isJournal"]=isJournal
#X_featureVector["isWorkshop"]=isWorkshop
#X_featureVector=X_featureVector.drop(['publication_channel'], axis = 1)
#X_featureVector=X_featureVector.astype(float)
#
# Splitting dataset into train & test subsets
#X_train, X_test, y_train, y_test = train_test_split(X_featureVector, y, test_size=0.40)


X_train, X_test, y_train, y_test = train_test_split(oheX, y, test_size=0.40)
lreg = LogisticRegression(solver='lbfgs', class_weight='balanced',max_iter=1000)


#HYPERPARAMETER TUNING:
# uncomment this section to run hyperparameter tuning on the classifier
#solver = ['newton-cg', 'lbfgs', 'liblinear']
#penalty = ['l2']
#C = [100, 10, 1.0, 0.1, 0.01]
#
#parameters = {
#    "solver":solver,
#    "penalty":penalty,
#    "C":C
#}
#
#lrRandom=RandomizedSearchCV(estimator=lreg, param_distributions=parameters, n_iter=2, cv=2,verbose=2)
#lrRandom.fit(X_train, y_train)
#
#
#def display(results):
#    print("\n")
#    print(f'Best parameters are: {results.best_params_}')
#    print("\n")
#    mean_score = results.cv_results_['mean_test_score']
#    std_score = results.cv_results_['std_test_score']
#    params = results.cv_results_['params']
#    for mean,std,params in zip(mean_score,std_score,params):
#        print(f'{round(mean,3)} + or -{round(std,3)} for the {params}')
#        
#display(lrRandom)

  
lreg.fit(X_train, y_train)


#Predict the response for test dataset
y_pred = lreg.predict(X_test)
y_score = lreg.predict_proba(X_test)

#print(y_pred.shape)
#print(y_score.shape)

# confusion matrix
confusion = confusion_matrix(y_test, y_pred)
print("Confusion matrix:\n{}".format(confusion)) 

# Accuracy
accuracy = accuracy_score(y_test, y_pred)
print('\nAccuracy: ', accuracy)

# F1 score
f1Score = f1_score(y_test, y_pred, pos_label="yes")
print('\nF1 score: ', f1Score)


#convert y values to binary so they can be used to calculate precision-recall ROC/AUC
yTestBin=(y_test=="yes")*1
yPredBin=(y_pred=="yes")*1

precision, recall, thresholds = precision_recall_curve(yTestBin, y_score[:,1])
pr_auc = auc(recall, precision)
print('\nPrecision Recall AUC score: ',pr_auc,"\n")


# calculate the no skill line as the proportion of the positive class
no_skill = len(y[y==1]) / len(y)
# plot the no skill precision-recall curve
plt.plot([0, 1], [no_skill, no_skill], linestyle='--', label='No Skill')
# calculate model precision-recall curve
#precision, recall, _ = precision_recall_curve(y_test, pos_probs)
# plot the model precision-recall curve
plt.plot(recall, precision, marker='.', label='ROC Logistic')
# axis labels
plt.xlabel('Recall')
plt.ylabel('Precision')
# show the legend
plt.legend()
# show the plot
plt.show()


#FEATURE IMPORTANCE 2:
#store a zip object containing each feature and its corresponding feature importance score
#finalColumns=["best_match_score","fuzz_ratio","fuzz_partial_ratio","fuzz_token_sort_ratio","kmpMatch","BM_badCharMatch","rabinKarpMatch","isConference","isOther","isJournal","isWorkshop"]
#feature_importances = zip(finalColumns, lreg.coef_.flatten())
#
#scaling the coefficients by multiplying them by the coefficient of the corresponding feature.
#see: https://scikit-learn.org/stable/auto_examples/inspection/plot_linear_model_coefficient_interpretation.html
#seriesFI=(np.std(X_featureVector, 0)*lreg.coef_.flatten())
#listFI=list(zip(seriesFI.index, seriesFI))
#print(listFI)
#
#sum the feature importances of the individual publication channels.
#append this sum to the list of feature importances
#conferenceTuple=listFI[7]
#otherTuple=listFI[8]
#journalTuple=listFI[9]
#workshopTuple=listFI[10]
#publicationChannelScore=conferenceTuple[1]+otherTuple[1]+journalTuple[1]+workshopTuple[1]
#del listFI[7:]
#listFI.append(tuple(("publicationChannel", publicationChannelScore)))

#plot the feature importances graphically
#x = range(8)
#plt.bar(x, [val[1] for val in listFI], align='center')
#plt.xticks(x,[val[0] for val in listFI])
#plt.xticks(rotation=90)
#plt.show()

