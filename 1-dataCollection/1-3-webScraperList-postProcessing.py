# -*- coding: utf-8 -*-

#takes in "conferenceNamesScraper.csv" - list of scraped conference venues
#removes null entries and outputs cleaned list as 'conferenceNamesScraper-postProcessing.csv'

import pandas as pd
import numpy as np

if __name__ == '__main__':
    #takes in list of scraped conference venues
    df = pd.read_csv("conferenceNamesScraper.csv")
    #print(df)
    
    #remove empty cells by converting to NaN and calling dropna method
    df['0'].replace('', np.nan, inplace=True)
    df.dropna(subset=['0'], inplace=True)
    #print(df)
    #df = pd.DataFrame(conferenceNames)
    #store processed conference name list
    df.to_csv('conferenceNamesScraper-postProcessing.csv', index=False)
    
    