# -*- coding: utf-8 -*-

#opens a chromium window and uses selenium to scrape conference names from researcher profiles
#stores these input conference names in 'conferenceNamesScraper.csv'
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd


#for PATH, enter your chromedriver.exe  install location here 
PATH = "C:\Program Files (x86)\Chromedriver\chromedriver.exe"

#initial values needed to access UCD CS researcher names + researcher profiles
nameSourceURL="https://www.ucd.ie/cs/people/academicstaff/"
rootURL="https://people.ucd.ie/"
#webpage = "https://people.ucd.ie/deepak.ajwani/publications"
urlExtensionOne = "?startFrom="
urlExtensionTwo = "&perPage=25&sort=typeAsc&favouritesFirst=true"
urlValue= ["0","25","50"]

researcherNames=[]
researcherNamesFinal=[]
conferenceNames=[]

#open chromium and access UCD CS reseracher directory
driver= webdriver.Chrome(PATH)
driver.get(nameSourceURL)
print(driver.title)

try:
        #wait for page to load
        element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH,'//button[@id="onetrust-accept-btn-handler"]'))).click()
        
        #once reseracher emails are loaded, scrape them and add to researcherNames list
        e = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "email")))
        emailList=driver.find_elements_by_class_name("email")
        
        for email in emailList:
            researcherNames.append(email.text)
        
        #move to next page in direccotry if possible
        try:
            nextLink = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT, ">"))).click()
            nextLinkAvailable=1
        except:
            print("Element is not clickable")
            
        #once all directory pages processed, exit
        while(nextLinkAvailable != 0):
            nextLinkAvailable=0
            element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "email")))
            emailList=driver.find_elements_by_class_name("email")
            
            for email in emailList:
                researcherNames.append(email.text)
            
            try:
                nextLink = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.LINK_TEXT, ">"))).click()
                nextLinkAvailable=1
            except:
                print("All pages processed")
                
except:
        driver.quit()
        
for name in researcherNames:
    substringName=name.split('@',1)[0]
    researcherNamesFinal.append(substringName)

#print(researcherNamesFinal)
    

#for each researcher name that was scraped, create the URL accessing their research output page
for name in researcherNamesFinal:
    errortext="An unexpected error occurred"
    offset=0
    urlOffset=str(offset)
    currentURL=rootURL+name+"/publications"+urlExtensionOne+urlOffset+urlExtensionTwo
    
    #open research output page and wait to load
    driver.get(currentURL)
    time.sleep(3)
    #this code handles "An unexpected error occurred" page that sometimes appears when loading a new profile
    error = driver.find_elements_by_xpath("//*[contains(text(), 'An unexpected error occurred')]")
    while (len(error) > 0):
        driver.refresh()
        time.sleep(3)
        error = driver.find_elements_by_xpath("//*[contains(text(), 'An unexpected error occurred')]")
    #next button is not clickable so have to manually edit the url instead  
    noResult=driver.find_elements_by_xpath("//*[contains(text(), 'There is no information to display.')]")
    while (len(noResult) == 0):
        #once page contents have loaded, use the class_name to scrape all conference venue elements from the page
        try:
            profile = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CLASS_NAME, "profile__pageContents___3IyqG"))
            )

            entries = profile.find_elements_by_class_name("publication__citation___OEiE2")
            #retrieve the conferene venue string from the element and add it to the list of conference names
            for entry in entries:
                listStrings = entry.text.split(' ', 1)
                if (len(listStrings) > 1):
                    substringEntry = entry.text.split(" ", 1)[1]
                    substringEntry=substringEntry[8:]
                    print(substringEntry)
                    conferenceNames.append(substringEntry)
            #use URL offset to move to the next page of research outputs
            offset+=25
            urlOffset=str(offset)
            currentURL=rootURL+name+"/publications"+urlExtensionOne+urlOffset+urlExtensionTwo
            driver.get(currentURL)
            time.sleep(3)
            noResult=driver.find_elements_by_xpath("//*[contains(text(), 'There is no information to display.')]")
        #some researcher pages dont exist and throw an error, this is handled here
        except:
            print("PAGE FAILURE: " + currentURL)
            break

#store list of conference names in csv and exit browser
df = pd.DataFrame(conferenceNames)
df.to_csv('conferenceNamesScraper.csv')
driver.quit()
