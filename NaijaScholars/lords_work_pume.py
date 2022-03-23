###neccesary libraries..........Python 3.6.x adviseable to use
from os import altsep
from bs4 import BeautifulSoup
from requests_html import HTMLSession
import json
import requests
from os.path  import basename
import os

house = []
#function to extract questions

def downloadImage(imgUrl,struct,num):
    path = createNewDir(struct,num)
    
    with open(os.path.join(path,basename(imgUrl)), "wb") as f:
        
        f.write(requests.get(imgUrl).content)

def createNewDir(struct,num):
    path = os.path.join(type_exam,school,subject,struct,str(year),str(num))
    if not os.path.exists(path):
        os.makedirs(path)
    return path


def extract(soup,session):
    
    if(soup != "" and session != ""):
        results = soup.find_all("div", class_="question_block")
        for question in results:
            question_details = {}
            correct_option  = question.find(id="ans-label")
            question_details["correctOption"] = correct_option.text[0:1]
            question_text = question.find("div",class_="question_text")
            question_details["slug"] = school
            question_details["structure"] = "OBJECTIVE"
            number =  question.find("h3")
            question_details["number"] = int(number.text.strip().split(" ")[1])
            image_url = getImageUrl(question_text)
            if image_url != None:
                question_details["imageUrl"] = image_url
                downloadImage(image_url,question_details["structure"],question_details["number"])
            else:
                question_details["imageUrl"] = None
            question_details["text"] = question_text.get_text("\n")
            
            explanation_div = question.find("div",class_="q_explanation")
            explanation = explanation_div.find("div",class_="q_explanation_text table-responsive")
            if(explanation != None):
                question_details["explanation"] = {"text":explanation.text}
            else:
                question_details["explanation"] = {"text":None}

            
            #find all  options
            soup_options_parent = question.find(class_="question_content table-responsive")
            soup_options = soup_options_parent.find_all("p")
            
            options = []
            #majority format
            for paragraph in soup_options:
               if ")" in paragraph.text:
                   option = {}
                   option["option"] = paragraph.text[0:1]
                   option["text"] = paragraph.text[3:]
                   option_image = paragraph.find("img")
                   image_url = getImageUrl(paragraph)
                   if image_url != None:
                       option["imageUrl"] = image_url
                       downloadImage(image_url,question_details["structure"],question_details["number"])
                   else:
                       option["imageUrl"] = None
                   options.append(option)
##


            #special format
            # soup_options = soup_options_parent.find_all("div",class_="q_option")
            # for paragraph in soup_options:
            #     opt, txt = paragraph.find("span").text[0:1], paragraph.find("div").text
            #     option = {}
            #     option["option"] = opt
            #     option["text"] = txt
            #     option_image = paragraph.find("img")
            #     option["imageUrl"] = option_image
            #     image_url = getImageUrl(paragraph)
            #     if image_url != None:
            #         option["imageUrl"] = image_url
            #         downloadImage(image_url,question_details["structure"],question_details["number"])
            #     else:
            #         option["imageUrl"] = None

            #     if(option_image != None ):
            #          if (str(option_image).find("class=") == -1):
            #              #option["imageUrl"] = option_image["src"] to e worked upon
            #              option["imageUrl"] = None
            #     else:
            #          option["imageUrl"] = None
                # options.append(option)
            
            question_details["options"] = options
           
            
            question_details["subject"] = subject
            question_details["type"] = type_exam
            question_details["year"] = year
            
            
            print(question_details)

            house.append(question_details)
            
            #writeToFile(question_details)
            print()
        nextPage(soup,session)
        
        #convertToJson(house)
    else:
        print("Soup burnt or session expired")


def getImageUrl(soup):
    paragraphs = soup.find_all("p")
    image_url = None
    for paragarph in paragraphs:
        image_url = paragarph.find("img")
        if  image_url != None and "nscbt-mark" not in image_url:
            return image_url["src"]
    return image_url

#go to next page
def nextPage(soup,session,):
    if(soup != "" and session != ""):
        results = soup.find("ul",class_= "mg-0 pl-0")
        
        links = results.find_all("a")
        nextPage = None
        if links[-1].text.lower().strip() == "next »":
            nextPage = links[-1]["href"]
            cookSoup(nextPage,session)
        else:
             convertToJson(house)
             print("End of site reached,thank you for doing the lords work")
    else:
       
        print("Soup burnt or session expired")
       
#save objects as json        
def convertToJson(data):
     filename = "output_" + type_exam + "_" + str(month)+ "_" + school + "_" + str(year) + "_"  + subject + ".json"
     with open(filename, 'a') as outfile:
            json.dump(data, outfile,indent=2)
            
	
    
#get the html of the page
def cookSoup(url,session):
    resp = session.get(url)
    if(url != "" and session != ""):
        html = resp.html.html
        soup = BeautifulSoup(html, "html.parser")
        extract(soup,session)
    else:
        print("Soup burnt or session expired")

def writeToFile(text):
    with open("/Neco/Questions.txt",'a') as f:
        f.write(text+ "\n")
        

if __name__ == '__main__':
    school = "OOU"
    subject = "Use of English"
    type_exam = "POST-UTME"
    month = "FEB"
    years = [2002,2003,2004,2005,2007,2009]
    session = HTMLSession()
    # for i in years:
    #     house.clear()
    #     year = i
    #     base_url = "https://nigerianscholars.com/past-questions/economics/neco/year/" + str(i)
    #     cookSoup(base_url,session)

    house.clear()
    year = 2000
    base_url = "https://nigerianscholars.com/past-questions/english-language/oou/"
    cookSoup(base_url,session)
    
        
