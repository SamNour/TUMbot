import requests
import os.path
from datetime import datetime
import re



API_ENDPOINT = "https://campus.tum.de/tumonline/wbservicesbasic."

API_TOKENASK = "requestToken"
API_REQUEST_MONEY = "studienbeitragsstatus"
API_REQUEST_IDENTITY = "id"
API_REQUEST_EXAMS = "noten"

#API_TOKEN = "38082AA281635080C59ED8BCFE0B91F1"#meh forgot to remove so will cancel this put anyways

def extract_token_info(text):
    pattern = r'<token>(.*?)</token>'
    matches = re.findall(pattern, text)
    return matches

def requestOrReturnCachedApi(studentID):
    #check if file studentID.json exists:
    #   if yes: return file
    #   if no: request API and save to file

    if(os.path.isfile(studentID+".json")):
        return open(studentID+".json", "r").read()
    else:
        r = requests.get(url = API_ENDPOINT+API_TOKENASK, params = "?pUsername="+studentID+"&pTokenName=botTUM")
        if(r.status_code != 200):
            print("Error: Request failed with status code "+str(r.status_code))
            return None

        with open(studentID+".json", "w") as f:
            tokenOnly = extract_token_info(r.text)[0]
            f.write(tokenOnly)
            f.close()
    return tokenOnly

def requestMoney(API_TOKEN):
    r = requests.get(url = API_ENDPOINT+API_REQUEST_MONEY, params = "?pToken="+API_TOKEN)
    if(r.status_code != 200):
        print("Error: Request failed with status code "+str(r.status_code))
        return None
        #<?xml version="1.0" encoding="utf-8"?>
        #<rowset>
        #    <row>
        #        <soll>102</soll>
        #        <frist>2024-02-15</frist>
        #        <semester_bezeichnung>Sommersemester 2024</semester_bezeichnung>
        #        <semester_id>24S</semester_id>
        #    </row>
        #</rowset>
    #return only money:102, due date:2024-02-15, semester:Sommersemester 2024
    try:
        parsed = r.text[r.text.index("<soll>")+6:r.text.index("</soll>")]+","+r.text[r.text.index("<frist>")+7:r.text.index("</frist>")]+","+r.text[r.text.index("<semester_bezeichnung>")+22:r.text.index("</semester_bezeichnung>")]
        #parse the date into a date object:
        parts = parsed.split(',')

        # Extract the components
        number = int(parts[0])
        date_str = parts[1]
        semester = parts[2]

        # Convert date string to date object
        date_object = datetime.strptime(date_str, "%Y-%m-%d").date()

        # Create the tuple
        result_tuple = (number, date_object, semester)

        return result_tuple
    except Exception as e:
        print("Error: Parsing failed with error: "+str(e)+"\n"+r.text)
        return None

def requestName(API_TOKEN):
    r = requests.get(url = API_ENDPOINT+API_REQUEST_IDENTITY, params = "?pToken="+API_TOKEN)
    if(r.status_code != 200):
        print("Error: Request failed with status code "+str(r.status_code))
        return None
    try:
        parsed = r.text[r.text.index("<vorname>")+9:r.text.index("</vorname>")]+" "+r.text[r.text.index("<familienname>")+14:r.text.index("</familienname>")]
        return parsed
    except Exception as e:
        print("Error: Parsing failed")
        return None
    

def requestLastExamResult(API_TOKEN):
    r = requests.get(url = API_ENDPOINT+API_REQUEST_EXAMS, params = "?pToken="+API_TOKEN)
    if(r.status_code != 200):
        print("Error: Request failed with status code "+str(r.status_code))
        return None
    try:
        parsed = r.text[r.text.index("<lv_titel>")+10:r.text.index("</lv_titel>")]+": "+r.text[r.text.index("<uninotenamekurz>")+17:r.text.index("</uninotenamekurz>")]
        return parsed
    except Exception as e:  
        print("Error: Parsing failed with error: "+str(e)+"\n"+r.text)
        return None
    


API_TOKEN = requestOrReturnCachedApi("ge94gok")
print(requestMoney(API_TOKEN))
print(requestName(API_TOKEN))
print(requestLastExamResult(API_TOKEN))
#output:
#(102, datetime.date(2024, 2, 15), 'Sommersemester 2024')
#Max Mustermann
#Analysis 1: 1.0