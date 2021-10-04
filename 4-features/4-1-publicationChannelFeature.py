# -*- coding: utf-8 -*-

import pandas as pd

#takes "matchedExamples-100-400-leftFile-processed.csv" as input.
#determine if a keyword is present in the entry string.
#if a keyword is present then assign the entry with the corresponding publication medium (conference,journal,workshop,book chapter)
#if no keywords are found then assing the entry the general term "Other"
#output values are stored in 'matchedExamples-100-400-publication1-labels.csv'

#add a publication channel column to the input file
featuresDf=pd.DataFrame(columns=['publication_channel'])
trainingData=pd.read_csv('matchedExamples-100-400-leftFile-processed.csv')
mergedDf=pd.concat([trainingData,featuresDf])

#define the keywords for each publication medium
#all keywords are in lowercase to avoid missing matches due to case difference
conferenceWordList=['proceedings', 'conference', 'symposium']
journalWordList=['journal', 'transactions', 'review']
workshopWordList=['workshop', 'workshops']
bookChapterList=['lecture notes in']

#only the input strings are needed to determine this feature
researcherName=mergedDf['researcher_name']

#for each input string, create a lowercase version
for name in researcherName:
    publicationAssigned=False
    elementPresent=False
    i=0
    nameLower=name.lower()
    
    #search the string for any keywords relating to Conferences. 
    elementPresent= [element for element in conferenceWordList if(element in nameLower)]
    if(bool(elementPresent)==True):
        while (i<researcherName[researcherName== name].size):
            
            #keyword is found, this entry is a Conference
            currentIndex=researcherName[researcherName== name].index[i]
            mergedDf['publication_channel'][currentIndex]="Conference"
            publicationAssigned=True
            i+=1
     
    #search the string for any keywords relating to Journals. if keyword is found, this entry is a Journal
    elementPresent= [element for element in journalWordList if(element in nameLower)]
    if(bool(elementPresent)==True):
        while (i<researcherName[researcherName== name].size):
            
            #keyword is found, this entry is a Journal
            currentIndex=researcherName[researcherName== name].index[i]
            mergedDf['publication_channel'][currentIndex]="Journal"
            publicationAssigned=True
            i+=1
        
    #search the string for any keywords relating to Workshops. if keyword is found, this entry is a Workshop
    elementPresent= [element for element in workshopWordList if(element in nameLower)]
    if(bool(elementPresent)==True):
        while (i<researcherName[researcherName== name].size):
            
            #keyword is found, this entry is a Workshop
            currentIndex=researcherName[researcherName== name].index[i]
            mergedDf['publication_channel'][currentIndex]="Workshop"
            publicationAssigned=False
            i+=1
    
    #search the string for any keywords relating to Book Chapters. if keyword is found, this entry is a Book Chapter
    elementPresent= [element for element in bookChapterList if(element in nameLower)]
    if(bool(elementPresent)==True):
        while (i<researcherName[researcherName== name].size):
            
            #keyword is found, this entry is a Book Chapter
            currentIndex=researcherName[researcherName== name].index[i]
            mergedDf['publication_channel'][currentIndex]="Book Chapter"
            publicationAssigned=True
            i+=1
        
    #if no keywords are found then publication medium cannot be determined, assign the entry as "Other"
    if(publicationAssigned==False):
        while (i<researcherName[researcherName== name].size):
            
            #no keyword found, this entry is assigned as Other
            currentIndex=researcherName[researcherName== name].index[i]
            mergedDf['publication_channel'][currentIndex]="Other"
            publicationAssigned=True
            i+=1
        

print("OUTPUTTING PUBLICATION CHANNEL FEATURES")
mergedDf=mergedDf[['publication_channel']]
mergedDf.to_csv('matchedExamples-100-400-publication1-labels.csv', index=False) #output feature values