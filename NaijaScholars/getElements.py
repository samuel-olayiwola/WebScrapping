###neccesary libraries..........Python 3.6.x adviseable to use
from os import altsep, stat
from select import select
from bs4 import BeautifulSoup
from requests_html import HTMLSession
import json
import requests
from os.path  import basename
import os
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time
from openpyxl import Workbook  
  
wb = Workbook()  
sheet = wb.active  
  


house = []



def writeToFile(text):
    with open("churchByLocalGovt.txt",'a') as f:
        f.write(text+ "\n")

driver = webdriver.Edge(r'C:\Users\Anonymous\Documents\New folder\msedgedriver.exe')
driver.get('https://ecitibiz.interior.gov.ng/Marriage/Apply#part2')
time.sleep(60)


selectState = Select(driver.find_element_by_id("drpstate"))
for state in selectState.options:
    detail = []
    print("\n\n\n")
   
    if(state.text.lower().strip() == "select"):
        continue
    else:
       
        selectState.select_by_value(state.get_attribute("value"))
        selectLocalGovt = Select(driver.find_element_by_id("drpMarriageLocalgovernmentArea"))
        
        for localGovt in selectLocalGovt.options:
             if(state.text.lower().strip() == "select"):
                continue
             else:
                selectLocalGovt.select_by_value(localGovt.get_attribute("value"))
                time.sleep(3)
                selectParish = Select(driver.find_element_by_id("drpCelebCenter"))
                for parish in selectParish.options:
                    if parish.text.lower().strip() == "select":
                        continue
                    else:
                        detail.append(state.text)
                        detail.append(localGovt.text)
                        detail.append(parish.text)
                        house.append(detail)
                        detail=[]
                    
                        data = tuple(house)
                        for i in data:  
                            sheet.append(i)  
                            wb.save('appending.xlsx')  
                            house = []

    




            

        
        
            
