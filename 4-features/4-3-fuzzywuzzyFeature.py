# -*- coding: utf-8 -*-

#takes "matchedExamples-100-400-leftFile-processed.csv" and "matchedExamples-100-400-rightFile.csv" as input.
#compares the string pairs of each file using 3 methods from the fuzzywuzzy package:
#fuzz_ratio, fuzz_partial_ratio and fuzz_token_sort_ratio
#for each comparison a score is outputted depending on how similar the strings are and the method being used.
#the scores go from 0 to 100 (in increasing similarity)
#output values are stored in "matchedExamples-100-400-fuzzywuzzy3-scores.csv"
#fuzzywuzzy uses levenshtein distance:
#https://towardsdatascience.com/fuzzy-string-matching-in-python-68f240d910fe

from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import pandas as pd

#define input files and number of entries
leftFile = pd.read_csv("matchedExamples-100-400-leftFile-processed.csv")
rightFile = pd.read_csv("matchedExamples-100-400-rightFile.csv")
numberEntries=leftFile.size

#convert the entries into strings
leftFile = leftFile.astype(str)
rightFile = rightFile.astype(str)
leftFile=leftFile.values.tolist()
rightFile=rightFile.values.tolist()

counter=0
resultsList = []
cols = ["fuzz_ratio", "fuzz_partial_ratio", "fuzz_token_sort_ratio"]
mergedResults = pd.DataFrame(columns=cols)

#for each pair of entries
while (counter<numberEntries):
        leftString=leftFile[counter][0]
        rightString=rightFile[counter][0]
        
        #call each fuzzywuzzy method on the pair of strings and store the resulting value
        ratioScore=fuzz.ratio(leftString,rightString)
        partialRatioScore=fuzz.partial_ratio(leftString,rightString)
        tokenSortRatioScore=fuzz.token_sort_ratio(leftString,rightString)
        newRow = {'fuzz_ratio':ratioScore, 'fuzz_partial_ratio':partialRatioScore, 'fuzz_token_sort_ratio':tokenSortRatioScore}
        
        #add the result to the results df
        #print(newRow)
        mergedResults = mergedResults.append(newRow, ignore_index = True)
        counter+=1

#output feature values
print("OUTPUTTING FUZZYWUZZY SCORES")
mergedResults.to_csv("matchedExamples-100-400-fuzzywuzzy3-scores.csv", index=False)