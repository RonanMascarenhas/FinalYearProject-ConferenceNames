# -*- coding: utf-8 -*-

#takes "matchedExamples-100-400-leftFile-processed.csv" and "matchedExamples-100-400-rightFile.csv" as input.
#compares the strings of each file using the Bad Character heuristic of Boyer-Moore algorithm.
#if substring is present then 1 is returned, otherwise 0 is returned.
#output values are stored in "matchedExamples-100-400-BM_badChar5-scores.csv"
#this implementation is based on: https://www.geeksforgeeks.org/boyer-moore-algorithm-for-pattern-searching/

#rigtString=inputString=pat
#leftString=obrssString=txt

import pandas as pd

NO_OF_CHARS = 256

def badCharHeuristic(string, size):

	# Initialize all occurrence as -1
	badChar = [-1]*NO_OF_CHARS

	# Fill the actual value of last occurrence
	for i in range(size):
		badChar[ord(string[i])] = i;

	# retun initialized list
	return badChar

def BM_badChar_search(txt, pat):
    m = len(pat)
    n = len(txt)
    badChar = badCharHeuristic(pat, m)
    s = 0
    while(s <= n-m):
        j = m-1
        while j>=0 and pat[j] == txt[s+j]:
            j -= 1
        if j<0:
            #print("Pattern occur at shift = {}".format(s))
            s += (m-badChar[ord(txt[s+m])] if s+m<n else 1)
            return(1)
        else:
            s += max(1, j-badChar[ord(txt[s+j])])
    #print("NO MATCH FOUND")
    return(0)

# main method that calls the Bad Character Heuristic
def main():
    leftFile = pd.read_csv("matchedExamples-100-400-leftFile-processed.csv")
    rightFile = pd.read_csv("matchedExamples-100-400-rightFile.csv")
    numberEntries=leftFile.size
    
    #convert entries into list of strings
    leftFile = leftFile.astype(str)
    rightFile = rightFile.astype(str)
    leftFile=leftFile.values.tolist()
    rightFile=rightFile.values.tolist()
    
    counter=0
    cols = ["BM_badCharMatch"]
    mergedResults = pd.DataFrame(columns=cols)
    
    #for each pair of strings, call the Bad Char Heurisitc to determine if substring is present
    while (counter<numberEntries):
            leftString=leftFile[counter][0]
            rightString=rightFile[counter][0]
            #print(rightString,leftString)
            
            #returns 0 if match NOT found, 1 if match IS found
            matchFound=BM_badChar_search(leftString,rightString)
            newRow = {'BM_badCharMatch':matchFound}
            mergedResults = mergedResults.append(newRow, ignore_index = True)       #add the result to the results df
            
            counter+=1
            
    print("OUTPUTTING BOYER MOORE SCORES")
    mergedResults.to_csv("matchedExamples-100-400-BM_badChar5-scores.csv", index=False)     #output feature values
 
if __name__ == '__main__':
    main()
    