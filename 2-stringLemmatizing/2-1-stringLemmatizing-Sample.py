# -*- coding: utf-8 -*-

#takes as input "matchedExamples-100-400-leftFile.csv" - the list of 500+ conference strings that will be used as training/test data
#remove all occurrences of "noise" terms from strings like punctuation, numbers and ordinal adverbs (e.g. 1st, 2nd...)
#stop words are kept
#returns a list of lemmatized versions of the confernce strings, stores it as 'matchedExamples-100-400-leftFile-processed.csv'

import pandas as pd
import re
import string

if __name__ == '__main__':
    #store list of 500+ conference strings that will be used as training/test data in dataframe
    df = pd.read_csv("matchedExamples-100-400-leftFile.csv")
    
    #output number of conference names in list for reference
    numberConferenceNames=len(df.index)
    print("number of conference names: ",numberConferenceNames)
    counter=0
    
    #for each conference stirng, remove all punctuation from the string
    while (counter<numberConferenceNames):
        currentConferenceName=df.iloc[counter,0]
        currentConferenceName=currentConferenceName.translate(str.maketrans('', '', string.punctuation))
        
        #split the resuting string into words
        currentNameSplit=currentConferenceName.split()
        currentNameFinal=""
        
        #remove all ordinal adverbs + numbers from strings using regex and substitution
        #then merge the remaining words back into a string
        for index,word in enumerate(currentNameSplit):
            numericRegex=re.compile(r'\b\d+(st|nd|rd|th)')
            wordNumberSubbed=re.sub(numericRegex, "", word)
            wordResult = ''.join(i for i in wordNumberSubbed if not i.isdigit())
            currentNameSplit[index]=wordResult
            
        for word in currentNameSplit:
            currentNameFinal+=word+' '
        if (" th " in currentNameFinal):
            currentNameFinal=currentNameFinal.replace(" th ", " ")
        if (" st " in currentNameFinal):
            currentNameFinal=currentNameFinal.replace(" st ", " ")
        if (" rd " in currentNameFinal):
            currentNameFinal=currentNameFinal.replace("rd ", " ")
        if (" nd " in currentNameFinal):
             currentNameFinal=currentNameFinal.replace(" nd ", " ")
        df.iloc[counter,0]=currentNameFinal
        counter+=1
        
    #store list of lemmatized versions of the confernce strings in csv
    print(df)
    df.to_csv('matchedExamples-100-400-leftFile-processed.csv', index=False)