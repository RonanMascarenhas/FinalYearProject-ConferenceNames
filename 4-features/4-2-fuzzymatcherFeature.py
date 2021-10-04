# -*- coding: utf-8 -*-

#takes "matchedExamples-100-400-leftFile-processed.csv" and "matchedExamples-100-400-rightFile.csv" as input.
#compares the string pairs of each file using the fuzzymatcher approximate string matching package
#for each pair a score is outputted depending on how similar the strings are.
#if the similarity is too low then a score of -1 is assigned.
#output values are stored in "matchedExamples-100-400-fuzzymatcher2-scores.csv"
#fuzzymatcher uses jaro-winkler distance:
#https://github.com/fredeil/FuzzyMatcher

import pandas as pd
import fuzzymatcher

if __name__ == '__main__':
    #define the columns in each file on which the comparison is being made
    left_on="researcher_name"
    right_on = "obrss_name"
    
    #define input files and number of entries
    leftFile = pd.read_csv("matchedExamples-100-400-leftFile-processed.csv")
    rightFile = pd.read_csv("matchedExamples-100-400-rightFile.csv")
    numberEntries=leftFile.size
    
    resultsList = []
    counter=0
    
    cols = ["best_match_score", "researcher_name", "obrss_name"]
    mergedResults = pd.DataFrame(columns=cols)
    
    #for each pair of entries
    while (counter<numberEntries):
        
        #convert the entries into strings
        one=leftFile.iloc[[counter],[0]]
        two=rightFile.iloc[[counter],[0]]
        oneValue = one.astype(str)
        oneValue=oneValue.values.tolist()
        twoValue = two.astype(str)
        twoValue =twoValue.values.tolist()
        
        #call the fuzzymatcher method on the pair of strings and store the resulting value
        cols = ["best_match_score", "researcher_name", "obrss_name"]
        matched_results = fuzzymatcher.fuzzy_left_join(one,two,left_on,right_on)
        value= matched_results.values.tolist()
        
        #if not value is present then similarity is too low, assign score of -1
        if(value[0][0]is None):         
            data = {'best_match_score':-1,'researcher_name':oneValue[0][0],'obrss_name':twoValue[0][0]}
            matched_results = pd.DataFrame(data,index=[0])
            
        
        matched_results =matched_results[cols]
        #add the result to the results df
        mergedResults = mergedResults.append(matched_results, ignore_index = True)
        counter+=1
        
    #output feature values
    print("OUTPUTTING FUZZYMATCHER SCORES")
    fuzzyMatcherScores=mergedResults["best_match_score"]
    fuzzyMatcherScores.to_csv("matchedExamples-100-400-fuzzymatcher2-scores.csv", index=False)
    