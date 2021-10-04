# -*- coding: utf-8 -*-

#takes "matchedExamples-100-400-leftFile-processed.csv" and "matchedExamples-100-400-rightFile.csv" as input.
#compares the strings of each file using the Rabin-Karp algorithm.
#if substring is present then 1 is returned, otherwise 0 is returned.
#output values are stored in "matchedExamples-100-400-rabinKarp6-scores.csv"
#implementation based on: https://www.geeksforgeeks.org/rabin-karp-algorithm-for-pattern-searching/

# d is the number of characters in the input alphabet
d = 256

# pat -> pattern
# txt -> text
# q -> A prime number

#rigtString=inputString=pat
#leftString=obrssString=txt

import pandas as pd

def rabinKarpSearch(pat, txt, q):
    M = len(pat)
    N = len(txt)
    i = 0
    j = 0
    p = 0 # hash value for pattern
    t = 0 # hash value for txt
    h = 1
    #print("\nlength input:",M)
    #print("\nlength obrss:",N,"\n")
    if(M>N):
        #print("PATTERN LONGER THAN TEXT, EXITING\n")
        return(0)
    for i in range(M-1):
        h = (h*d)%q
    for i in range(M):
        p = (d*p + ord(pat[i]))%q
        t = (d*t + ord(txt[i]))%q
    for i in range(N-M+1):
        if p==t:
            for j in range(M):
                if txt[i+j] != pat[j]:
                    break
                else: j+=1
            if j==M:
                #print("Pattern found at index " ,str(i))
                return(1)
        if i < N-M:
            t = (d*(t-ord(txt[i])*h) + ord(txt[i+M]))%q
            if t < 0:
                t = t+q
    #print("NO MATCH FOUND")
    return(0)

#convert entries into list of strings
leftFile = pd.read_csv("matchedExamples-100-400-leftFile-processed.csv")
rightFile = pd.read_csv("matchedExamples-100-400-rightFile.csv")
numberEntries=leftFile.size
leftFile = leftFile.astype(str)
rightFile = rightFile.astype(str)
leftFile=leftFile.values.tolist()
rightFile=rightFile.values.tolist()

counter=0
cols = ["rabinKarpMatch"]
mergedResults = pd.DataFrame(columns=cols)

# A prime number
q = 101

#for each pair of strings, call the KMP algorithm to determine if substring is present
while (counter<numberEntries):
        leftString=leftFile[counter][0]
        rightString=rightFile[counter][0]
        
        #returns 0 if match NOT found, 1 if match IS found
        matchFound=rabinKarpSearch(rightString,leftString,q)
        newRow = {'rabinKarpMatch':matchFound}
        mergedResults = mergedResults.append(newRow, ignore_index = True)    #add the result to the results df
        
        counter+=1
        
print("OUTPUTTING RABIN KARP SCORES")
mergedResults.to_csv("matchedExamples-100-400-rabinKarp6-scores.csv", index=False)  #output feature values

