# -*- coding: utf-8 -*-

#Takes as input "master-channel-list-2019.csv" - the OBRSS master list of conference names
#Returns a reduced list containing conference+journal names that relate to Computer Science
#This stores this list in csv format as "obrssConferenceNameList.csv"

import pandas as pd
from unidecode import unidecode
import re

def preProcess(column):
    #data cleaning using unidecode and regex (casing, extra spaces, quotes and new lines)
    column = unidecode(column)
    column = re.sub('\n', ' ', column)
    column = re.sub('-', '', column)
    column = re.sub('/', ' ', column)
    column = re.sub("'", '', column)
    column = re.sub(',', '', column)
    column = re.sub(':', ' ', column)
    column = re.sub('  +', ' ', column)
    
    return column

if __name__ == '__main__':
    
    #store obrss list as dataframe
    df = pd.read_csv("master-channel-list-2019.csv")

    #remove any entries that don't refer to conferences or journals
    dfEdited = df[(df['Publication channel'] == "Conference") | (df['Publication channel'] == "Conference Series") | (df['Publication channel'] == "Journal")]

    #make a dataframe consisting of all conferences related to computer science
    dfConSourceCS = dfEdited[(dfEdited['Publication channel'] == "Conference") & ((dfEdited['Source / Panel name'] == "Computer Science") & (dfEdited['Discipline(s)'] != "Computer Science"))]
    dfConDiscCS = dfEdited[(dfEdited['Publication channel'] == "Conference") & ((dfEdited['Source / Panel name'] != "Computer Science") & (dfEdited['Discipline(s)'] == "Computer Science"))]
    dfConBothCS = dfEdited[(dfEdited['Publication channel'] == "Conference") & ((dfEdited['Source / Panel name'] == "Computer Science") & (dfEdited['Discipline(s)'] == "Computer Science"))]
    
    #make a dataframe consisting of all conference series related to computer science
    dfConseriesSourceCS = dfEdited[(dfEdited['Publication channel'] == "Conference Series") & ((dfEdited['Source / Panel name'] == "Computer Science") & (dfEdited['Discipline(s)'] != "Computer Science"))]
    dfConseriesDiscCS = dfEdited[(dfEdited['Publication channel'] == "Conference Series") & ((dfEdited['Source / Panel name'] != "Computer Science") & (dfEdited['Discipline(s)'] == "Computer Science"))]
    dfConseriesBothCS = dfEdited[(dfEdited['Publication channel'] == "Conference Series") & ((dfEdited['Source / Panel name'] == "Computer Science") & (dfEdited['Discipline(s)'] == "Computer Science"))]

    #make a dataframe consisting of all journals related to computer science
    dfJournalSourceCS = dfEdited[(dfEdited['Publication channel'] == "Journal") & ((dfEdited['Source / Panel name'] == "Computer Science") & (dfEdited['Discipline(s)'] != "Computer Science"))]
    dfJournalDiscCS = dfEdited[(dfEdited['Publication channel'] == "Journal") & ((dfEdited['Source / Panel name'] != "Computer Science") & (dfEdited['Discipline(s)'] == "Computer Science"))]
    dfJournalBothCS = dfEdited[(dfEdited['Publication channel'] == "Journal") & ((dfEdited['Source / Panel name'] == "Computer Science") & (dfEdited['Discipline(s)'] == "Computer Science"))]
    
    #concatenate dataframes to make merged dataframe of all conference+conference series+journals names that relate to Computer Science
    dfConFinal = pd.concat([dfConSourceCS, dfConDiscCS])
    dfConFinal = pd.concat([dfConFinal, dfConBothCS])
    dfConseriesFinal = pd.concat([dfConseriesSourceCS, dfConseriesDiscCS])
    dfConseriesFinal = pd.concat([dfConseriesFinal, dfConseriesBothCS])
    dfJournalFinal = pd.concat([dfJournalSourceCS, dfJournalDiscCS])
    dfJournalFinal = pd.concat([dfJournalFinal, dfJournalBothCS])
    
    dfFinal = pd.concat([dfConFinal, dfConseriesFinal])
    dfFinal = pd.concat([dfFinal, dfJournalFinal])
    dfFinal.to_csv("obrssConferenceNameList.csv")       #store final list in csv
