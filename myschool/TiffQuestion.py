from logging import exception
from bs4 import BeautifulSoup
from requests_html import HTMLSession
import json
import requests
from os.path  import basename
import os


house =[]
def downloadImage(imgUrl,struct,num):
    try:
        path = createNewDir(struct,num)
        
        with open(os.path.join(path,basename(imgUrl)), "wb") as f:
            
            f.write(requests.get(imgUrl).content)
    except exception as e:
        print(e.message,e.args)
        
def createNewDir(struct,num):
    try:
        path = os.path.join(exam_type,subject,structure,str(exam_year),str(num))
        if not os.path.exists(path):
            os.makedirs(path)
        return path
    except exception as e:
        print(e.message,e.args)


def extract(soup,session):
    try:    
        if(soup != None and session != None):
            results = soup.find_all("div",class_="media question-item mb-4")
            for item in results:
                question_details = {}
                correctAnswer,explanation = getCorrectAnswerExplanation(item)
                question_details["correctOption"] = correctAnswer
                question_details["explanation"] = {"text":explanation}
                question_Text = getQuestion(item)
                question_details["text"] = question_Text
                question_details["structure"] = structure
                number = getNumber(item)
                question_details["number"] = int(number)
                imageUrl = getImageUrl(item,number)
                question_details["imageUrl"] = imageUrl
                options = getOptions(item,number)
                question_details["options"] = options

                question_details["subject"] = subject
                question_details["type"] = exam_type
                question_details["year"] = exam_year


                print(question_details)
                house.append(question_details)
                print("\n\n")
            nextPage(soup,session)
            
    except exception as e:
        print(e.message,e.args)





def nextPage(soup,session):
    if(soup != "" and session != ""):
        results = soup.find("ul",class_= "pagination flex-wrap")
        
        links = results.find_all("a")
        nextPage = None
        if links[-1].text.lower().strip() == "»":
            nextPage = links[-1]["href"]
            next,newSession = cookSoup(nextPage,session)
            extract(next,session)
        else:
             convertToJson(house)
             print("End of site reached,thank you for tiffing questions")
    else:
       
        print("Soup burnt or session expired")

def convertToJson(data):
     filename = "output_" + exam_type + "_" + str(exam_year) + "_"  + subject + ".json"
     with open(filename, 'a') as outfile:
            json.dump(data, outfile,indent=2)
            
       
def getOptions(item,num):
    try:
        options = []
        result = item.find("ul",class_="list-unstyled")
        optionsResult = result.find_all("li")
        for val in optionsResult:
            option = {}
            option["option"] = val.find("strong").text.replace(".","").strip()
            option["text"] = val.text.strip()
            #option_image = val.find("img")
            image_url = getImageUrl(item,num)
            if image_url != None:
                option["imageUrl"] = image_url
                #downloadImage(image_url,question_details["structure"],question_details["number"])
            else:
                option["imageUrl"] = None
            options.append(option)
        return options
    except exception as e:
        print(e.message,e.args)



def getNumber(item):
    try:
        result = item.find("div",class_="question_sn bg-danger mr-3")
        number = result.text.strip()
        return number
    except exception as e:
        print(e.message,e.args)
        

def getImageUrl(item,num):
    image = item.find("img")
    if not image == None :
        url =image["src"]
        downloadImage(url,structure,num)
        return url
    else:
        return None



def getQuestion(item):
    try:
        result = item.find("div",class_="question-desc mt-0 mb-3")
        question = result.find("p")
        text = question.text.replace('"',"").strip() 
        return text
    except exception as e:
        print(e.message,e.args)
        
def getCorrectAnswerExplanation(item):
    try:
        if(item != None):
            answerLink = item.find("a")
            session = HTMLSession()
            base_url = answerLink['href']
            soup,newSession = cookSoup(base_url,session)
            if(soup != None and session != None):
                result =soup.select("div[class='mb-4']")
                if len(result) == 3:
                    answerResult = result[1].find("h5",class_="text-success mb-3")
                    explationResult = result[1].text
                else:
                    answerResult = result[0].find("h5",class_="text-success mb-3")
                    explationResult = result[0].text
                answer = answerResult.text.replace("Correct Answer: Option ","").strip()
                explanation = explationResult[explationResult.index("Explanation"):].strip()
                if explanation != None:
                    return answer,explanation
                else:
                    return answer,None
    except exception as e:
        print(e.message,e.args)
    





def cookSoup(url,session):
    try:
        resp = session.get(url)
        if(url != "" and session != ""):
            html = resp.html.html
            soup = BeautifulSoup(html, "html.parser")
            return soup,session
        else:
            print("Soup burnt or session expired")
    except exception as e :
        print(e.message,e.args)













if __name__ == '__main__':
    subject = "Civic Education"
    exam_type = "WAEC"
    structure = "OBJECTIVE"
    if structure == "OBJECTIVE":
        url_Struc = "obj"

    exam_year = 2021
    additional_url = subject.lower().replace(" ","-") + "?xam_type=" + exam_type.lower() + "&" + "exam_year=" + str(exam_year) + "&" + "type=" + url_Struc
    session = HTMLSession()
    base_url = "https://myschool.ng/classroom/" + additional_url
    soup,newSession = cookSoup(base_url,session)
    extract(soup,newSession)
    
        
