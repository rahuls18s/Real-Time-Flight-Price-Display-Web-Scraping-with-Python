from bs4 import BeautifulSoup
import requests
import datetime
import speech_recognition as sr
import smtplib
import pandas as pd
import pyttsx3
import time
import lxml


engine=pyttsx3.init("sapi5")
voices=engine.getProperty('voices')
engine.setProperty("voice",voices[0].id)
r = sr.Recognizer()

def say(audio):
    engine.setProperty("rate",110)
    engine.say(audio)
    engine.runAndWait()

def takecommand():
  with sr.Microphone() as source:
    r.adjust_for_ambient_noise(source,duration=3)
    print("Listening....")
    audio=r.listen(source)
    print("recorded")
    speech=r.recognize_google(audio)
    speech.lower()
    print(speech)
    return speech
  
def wishme():
    hour =int(datetime.datetime.now().hour)
    print(hour)
    if hour>=0 and hour <12:
        say("good morning")
    elif hour>=12 and hour <18:
        say("good evening")
    else:
        say("Hello")
    txt="""      I am your Airman, 
         I can provide you best flights and
         I can notify through mail if flight price is fallen
      """
    say(txt)
    print(txt)

wishme()

try:
 print("From where")
 say("from where")
 arr=takecommand()
 print("Where to:")
 say("where to")
 dep=takecommand()
except:
 print("""SORRY SIR DID'T HEAR THAT ...
      PLEASE TYPE """)
 dep=input("From where?:")
 arr=input("Where to:") 

url=f'https://www.google.com/travel/flights/flights-from-{dep}-to-{arr}.html'
re=requests.get(url)
res=re.content
soup=BeautifulSoup(res,'html.parser')

qt=[]
wt=[] 
et=[]
rt=[]  
tt=[]
divide=soup.find_all('li',class_="pIav2d")
for div in divide:
   flight_name=div.find("div",class_="sSHqwe tPgKwe ogfYpf").span.text
   qt.append(flight_name)

   duration=div.find("div",class_="Ak5kof").find("div",class_="gvkrdb AdWm1c tPgKwe ogfYpf").text
   wt.append(duration)

   r=div.find("div",class_="U3gSDe").span.text[1:].replace(',',"")
   et.append(r)

   flight_stop=div.find("div",class_="BbR8Ec").span.text
   rt.append(flight_stop)

   dep_time=div.find("div",class_="Ir0Voe").span.text
   tt.append(dep_time)

best=f"""BEST FLIGHTS FROM {dep} to {arr}

     """
print(best)
say(best)
dt={'FLIGHT NAME':qt,     
    'DURATION':wt,
    'PRICE':et,
    'FLIGHT_STOP':rt,
    'TIME':tt
}
details=pd.DataFrame(dt)
print(details[['FLIGHT NAME','DURATION','PRICE','FLIGHT_STOP','TIME']])

bt="""
        Best cheapest Flight
   """
print(bt)
say(bt)
rate=soup.find("div",class_="BOyk6b")
lpr=rate.div.div.div.div.text
sav=lpr.encode('utf-8').strip()
print(lpr)
say(lpr)

pr=soup.find('li',class_="pIav2d")
flight_name=div.find("div",class_="sSHqwe tPgKwe ogfYpf").span.text

duration=div.find("div",class_="Ak5kof").find("div",class_="gvkrdb AdWm1c tPgKwe ogfYpf").text
r=pr.find("div",class_="U3gSDe").span.text[1:].replace(',',"")
price=int(r)

flight_stop=div.find("div",class_="BbR8Ec").span.text
dep_time=div.find("div",class_="Ir0Voe").span.text

mg=f"""
        FLIGHT NAME:{flight_name}
        DURATION:{duration}
        PRICE:{price}
        FLIGHT_STOP:{flight_stop}
        TIME:{dep_time}

"""
print(mg)
say(mg)

print("   To book now use this")
print(f"  https://www.makemytrip.com/flights/{dep}-{arr}-cheap-airtickets.html")

req="""I can notify best flight for you 
     To notify say yes or no """
print(req)
say(req)

rate=soup.find("div",class_="BOyk6b")
lpr=rate.div.div.div.div.div.div.text
print(lpr)
sav=lpr.encode('utf-8').strip()
print(sav)


mg=f"""{sav[0:25]}
        FLIGHT NAME:{flight_name}
        DURATION:{duration}
        PRICE:{price}
        FLIGHT_STOP:{flight_stop}

        "To book now use this"
        https://www.makemytrip.com/flights/{dep}-{arr}-cheap-airtickets.html
        """

print(mg)
print("***********")
mail_id=input("Enter your mail id:")
while True:
    main=smtplib.SMTP_SSL('smtp.gmail.com',465)
    sender="sample112py@gmail.com"
    password='kwjsjnfxyapfpjyt'
    rec=mail_id
    subject="Best Cheapest Flight"
    body="Ticket price is fallen"
    msg=f"""{subject}
        FLIGHT FROM {dep.upper()} to {arr.upper()}
            {mg}
            """
    main.login(sender,password)   
    main.ehlo()
    main.sendmail(sender,rec,msg)
    main.quit()
    print("msg sent")
    time.sleep(24*60*60)
    





