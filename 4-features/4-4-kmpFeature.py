# -*- coding: utf-8 -*-

import pandas as pd

#takes "matchedExamples-100-400-leftFile-processed.csv" and "matchedExamples-100-400-rightFile.csv" as input.
#compares the strings of each file using the KMP algorithm.
#if substring is present then 1 is returned, otherwise 0 is returned.
#output values are stored in "matchedExamples-100-400-kmpMatch4-scores.csv"
#kmp exact string match implementation. based on:
#https://www.geeksforgeeks.org/python-program-for-kmp-algorithm-for-pattern-searching-2/

    
#0 means match not found, 1 means match found
def KMPSearch(inputString, obrssString):
    lengthInput = len(inputString)
    lengthObrss = len(obrssString)
    
    #print(inputString,"\nlength input:",lengthInput)
    #print(obrssString,"\nlength obrss:",lengthObrss,"\n")

    if(lengthInput>lengthObrss):
        return(0)

    lps = [0]*lengthInput
    j = 0 # index for pat[]

    # Preprocess the pattern (calculate lps[] array)
    computeLPSArray(inputString, lengthInput, lps)

    i = 0 # index for txt[]
    while i < lengthObrss:
        if inputString[j] == obrssString[i]:
            i += 1
            j += 1

        if j == lengthInput:
            j = lps[j-1]
            return(1)

        # mismatch after j matches
        elif i < lengthObrss and inputString[j] != obrssString[i]:
            # Do not match lps[0..lps[j-1]] characters,
            # they will match anyway
            if j != 0:
                j = lps[j-1]
            else:
                i += 1
    
    return(0)

def computeLPSArray(inputString, lengthInput, lps):
	len = 0 # length of the previous longest prefix suffix

	lps[0] # lps[0] is always 0
	i = 1

	# the loop calculates lps[i] for i = 1 to M-1
	while i < lengthInput:
		if inputString[i]== inputString[len]:
			len += 1
			lps[i] = len
			i += 1
		else:
			# This is tricky. Consider the example.
			# AAACAAAA and i = 7. The idea is similar
			# to search step.
			if len != 0:
				len = lps[len-1]

				# Also, note that we do not increment i here
			else:
				lps[i] = 0
				i += 1


#convert entries into list of strings
leftFile = pd.read_csv("matchedExamples-100-400-leftFile-processed.csv")
rightFile = pd.read_csv("matchedExamples-100-400-rightFile.csv")
numberEntries=leftFile.size
leftFile = leftFile.astype(str)
rightFile = rightFile.astype(str)
leftFile=leftFile.values.tolist()
rightFile=rightFile.values.tolist()

counter=0
cols = ["kmpMatch"]
mergedResults = pd.DataFrame(columns=cols)

#for each pair of strings, call the KMP algorithm to determine if substring is present
while (counter<numberEntries):
        leftString=leftFile[counter][0]
        rightString=rightFile[counter][0]
        
        #returns 0 if match NOT found, 1 if match IS found
        matchFound=KMPSearch(rightString,leftString)
        newRow = {'kmpMatch':matchFound}
        mergedResults = mergedResults.append(newRow, ignore_index = True)    #add the result to the results df
        
        counter+=1
        
print("OUTPUTTING KMP SCORES")
mergedResults.to_csv("matchedExamples-100-400-kmpMatch4-scores.csv", index=False)   #output feature values
