import tkinter as tk
from tkinter import Entry
from datetime import datetime
import os
import glob
import time
import webbrowser

global smokingStatus
window = tk.Tk()
window.title("My Little Doctor")
width  = window.winfo_screenwidth()
height = window.winfo_screenheight()
window.resizable(width=False, height=False)

def callback(url):
    webbrowser.open_new(url)

def forget_children(window):
    _list = window.winfo_children()
    for item in _list :
        if item.winfo_children() :
            _list.extend(item.winfo_children())
    for item in _list:
        item.pack_forget()

def mailto(name, lastname, dateob, docname, docmail, nhsnum, remaindays):
    with open('chronicEmail.txt', 'r') as b:
        body = b.read()
        body = body.replace('docnam', docname)
        body = body.replace('name', name)
        body = body.replace('last', lastname)
        body = body.replace('dateob', dateob)
        body = body.replace('nhsnum', nhsnum)
        body = body.replace('remaindays', remaindays)
        body = body.replace(' ', '%20')
        body = body.replace('\n', '%0D')
    subject = "Repeat Prescription for "+name+' '+lastname
    webbrowser.open("mailto:%s?subject=%s&body=%s" % (docmail, subject, body))

def mailto1(name, lastname, dateob, docname, docmail, tele, condition):
    with open('chronicEmail1.txt', 'r') as b:
        body = b.read()
        body = body.replace('docnam', docname)
        body = body.replace('name', name)
        body = body.replace('last', lastname)
        body = body.replace('dateob', dateob)
        body = body.replace('telephone', tele)
        body = body.replace('condition', condition)
        body = body.replace(' ', '%20')
        body = body.replace('\n', '%0D')
    subject = "Chronic Illness not Responding to Medication for "+name+' '+lastname
    webbrowser.open("mailto:%s?subject=%s&body=%s" % (docmail, subject, body))

def mailto2(name, lastname, dateob, docname, docmail, nhsnum, disease):
    with open('chronicEmail2.txt', 'r') as b:
        body = b.read()
        body = body.replace('docnam', docname)
        body = body.replace('name', name)
        body = body.replace('last', lastname)
        body = body.replace('dateob', dateob)
        body = body.replace('nhsnum', nhsnum)
        body = body.replace('condition', disease)
        body = body.replace(' ', '%20')
        body = body.replace('\n', '%0D')
    subject = "Concern regarding my "+disease+" for "+name+' '+lastname
    webbrowser.open("mailto:%s?subject=%s&body=%s" % (docmail, subject, body))


def temperatureRead():
    os.system('modprobe w1-gpio')
    os.system('modprobe w1-therm')
    base_dir = '/sys/bus/w1/devices/'
    device_folder = glob.glob(base_dir + '28*')[0]
    device_file = device_folder + '/w1_slave'
    return device_file

def read_temp_raw(device_file):    
    f = open(device_file, 'r')
    lines = f.readlines() 
    f.close()
    return lines

def read_temp():
    device_file = temperatureRead()
    lines = read_temp_raw(device_file)
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_c, temp_f
    
def tempWindow():
    forget_children(window)
    tk.Label(window, text = "", font =('Calibri', 15)).pack()
    tk.Label(window, text = "Please hold the temperature sensor for 10 seconds\nand click Start below.", font =('Verdana', 15)).pack()
    tk.Label(window, text = "This may take some time.", font =('Verdana', 15)).pack()
    tk.Label(window, text = "", font =('Calibri', 15)).pack()
    tk.Button(window,text="Start", command=startReading, font =('Verdana', 15)).pack()
    tk.Button(window,text="Back", command=new, font =('Verdana', 15)).pack()

def startReading():
    def temperatureCalculations():
        forget_children(window)
        if readings[0] < 35:
            tk.Label(window, text = "", font =('Calibri', 15)).pack()
            tk.Label(window, text = "Your temperature is very low. Call Emergency Services\nif you are shivering as you may be suffering\n from Hypothermia.", font =('Verdana', 15)).pack()
        elif readings[0] >= 35 and readings[0] < 37:
            tk.Label(window, text = "", font =('Calibri', 15)).pack()
            tk.Label(window, text = "Your temperature is low. Drink warm fluids and\nstay warm!", font =('Verdana', 15)).pack()
        elif readings[0] >= 37 and readings[0] < 38:
            tk.Label(window, text = "", font =('Calibri', 15)).pack()
            tk.Label(window, text = "Your temperature is normal.\nYou should be healthy!", font =('Verdana', 15)).pack()
        elif readings[0] >= 38:
            tk.Label(window, text = "", font =('Calibri', 15)).pack()
            tk.Label(window, text = "Your temperature is high.\nYou may have a fever or infection.", font =('Verdana', 15)).pack()
        tk.Button(window,text="Retry", command=tempWindow, font =('Verdana', 15)).pack()
        tk.Button(window,text="Home", command=main, font =('Verdana', 15)).pack()

        
    forget_children(window)
    tk.Label(window, text = "", font =('Calibri', 15)).pack()
    time.sleep(15)
    readings = read_temp()
    tk.Label(window, text = "", font =('Calibri', 15)).pack()
    tk.Label(window, text = "Your temperature\n is"+str(readings[0])+"°C.", font =('Verdana', 15)).pack()
    tk.Button(window,text="Next", command=temperatureCalculations, font =('Verdana', 15)).pack()
    tk.Button(window,text="Retry", command=tempWindow, font =('Verdana', 15)).pack()

def diabetes():
    forget_children(window)
    tk.Label(window, text = "", font =('Calibri', 15)).pack()
    tk.Label(window, text = "Are you having any of the following issues?", font =('Verdana', 15)).pack()
    tk.Label(window, text = "", font =('Calibri', 15)).pack()
    tk.Button(window,text="My Blood Sugar is high despite Medication", command=noResponse1, font =('Verdana', 15)).pack()
    tk.Button(window,text="I think I may be developing an Infection", command=new, font =('Verdana', 15)).pack()
    tk.Button(window,text="I need a Repeat Prescription for my Medication", command=repeat, font =('Verdana', 15)).pack()
    tk.Button(window,text="Back", command=chronic, font =('Verdana', 15)).pack()

def asthma():
    forget_children(window)
    tk.Label(window, text = "", font =('Calibri', 15)).pack()
    tk.Label(window, text = "Are you having any of the following issues?", font =('Verdana', 15)).pack()
    tk.Label(window, text = "", font =('Calibri', 15)).pack()
    tk.Button(window,text="I have recurrent attacks despite Medication", command=noResponse2, font =('Verdana', 15)).pack()
    tk.Button(window,text="I think I may be developing a Chest Infection", command=new, font =('Verdana', 15)).pack()
    tk.Button(window,text="I need a Repeat Prescription for my Medication", command=repeat, font =('Verdana', 15)).pack()
    tk.Button(window,text="Back", command=chronic, font =('Verdana', 15)).pack()

def hypertension():
    forget_children(window)
    tk.Label(window, text = "", font =('Calibri', 15)).pack()
    tk.Label(window, text = "Are you having any of the following issues?", font =('Verdana', 15)).pack()
    tk.Label(window, text = "", font =('Calibri', 15)).pack()
    tk.Button(window,text="My Blood Pressure is high despite Medication", command=noResponse3, font =('Verdana', 15)).pack()
    tk.Button(window,text="I need a Repeat Prescription for my Medication", command=repeat, font =('Verdana', 15)).pack()
    tk.Button(window,text="Back", command=chronic, font =('Verdana', 15)).pack()

def new():
    forget_children(window)
    tk.Label(window, text = "", font =('Calibri', 15)).pack()
    tk.Label(window, text = "Do you have a temperature sensor\nattached to the Pi?", font =('Verdana', 15)).pack()
    tk.Label(window, text = "", font =('Calibri', 15)).pack()
    tempYes = tk.Button(window,text="Yes", command=tempWindow, font =('Verdana', 15)).pack()
    tempNo = tk.Button(window,text="No", command=startChat, font =('Verdana', 15)).pack()
    tk.Button(window,text="Back", command=main, font =('Verdana', 15)).pack()

def other():
    forget_children(window)
    def submitEmail2():
        name = Firstname.get()
        lastname = Surname.get()
        dateob = DOB.get()
        docname = doctorName.get()
        docmail = doctorEmail.get()
        nhsNum = nhsnum.get()
        Disease = disease.get()
        mailto2(name, lastname, dateob, docname, docmail, nhsNum, Disease)
        tk.Label(window, text = "", font =('Calibri', 15)).pack()
        tk.Label(window, text = "Your email should be open in your client.", font =('Verdana', 15)).pack()
        tk.Button(window,text="Back", command=main, font =('Verdana', 15)).pack()
    forget_children(window)
    tk.Label(window, text = "", font =('Calibri', 15)).pack()
    tk.Label(window, text = "Please enter your details below\nso someone from your GP practice can call:", font =('Verdana', 15)).pack()
    tk.Label(window, text = "", font =('Calibri', 15)).pack()
    tk.Label(window, text = "First Name:", font =('Verdana', 15)).pack()
    Firstname = Entry(window,width=40)
    Firstname.pack()
    tk.Label(window, text = "Surname:", font =('Verdana', 15)).pack()
    Surname = Entry(window,width=40)
    Surname.pack()
    tk.Label(window, text = "Date Of Birth (DD/MM/YYYY):", font =('Verdana', 15)).pack()
    DOB = Entry(window,width=40)
    DOB.pack()
    tk.Label(window, text = "NHS Number of Patient:", font =('Verdana', 15)).pack()
    nhsnum = Entry(window,width=40)
    nhsnum.pack()
    tk.Label(window, text = "Condition:", font =('Verdana', 15)).pack()
    disease = Entry(window,width=40)
    disease.pack()
    tk.Label(window, text = "Doctor's Surname:", font =('Verdana', 15)).pack()
    doctorName = Entry(window,width=40)
    doctorName.pack()
    tk.Label(window, text = "Doctor's Email:", font =('Verdana', 15)).pack()
    doctorEmail = Entry(window,width=40)
    doctorEmail.pack()
    tk.Button(window,text="Submit", command=submitEmail2, font =('Verdana', 15)).pack()

def lifestyle():
    def bmiCalc():
        def smoker():
            def alcohol():
                def alcoholCalc():
                    def airQuality():
                        def finalSubmission():
                            forget_children(window)
                            tk.Label(window, text = "Generating Report...", font =('Verdana', 15)).pack()
                            now = datetime.now()
                            formattedDate = now.strftime("%d-%m-%Y,%H:%M:%S")
                            filename = "lifestyleReport"+formattedDate+".txt"
                            with open(filename, 'a')as f:
                                f.write('--LIFESTYLE REPORT GENERATED AT'+str(formattedDate)+'--\nBMI: '+str(bmi)+'\nAre they a Smoker: '+str(smokingStatus)+'\nUnits of Alcohol Drunk per Week: '+str(alcoholUnits.get())+'\nAir Pollution Score: '+str(score.get())+'\n--REPORT GENERATED BY MY LITTLE DOCTOR--')
                            tk.Label(window, text = "Report Generated!", font =('Verdana', 15)).pack()
                            tk.Button(window,text="Home", command=main, font =('Verdana', 15)).pack()
                        forget_children(window)
                        tk.Label(window, text = "", font =('Calibri', 15)).pack()
                        tk.Label(window, text = "Visit the following site:", font =('Verdana', 15)).pack()
                        link3 = tk.Button(window,text="Air Pollution Calculator", font =('Verdana', 15))
                        link3.pack()
                        link3.bind("<Button-1>", lambda e: callback("https://addresspollution.org/"))
                        tk.Label(window, text = "What score did you receive?", font =('Verdana', 15)).pack()
                        score = Entry(window,width=40)
                        score.pack()
                        tk.Button(window,text="Submit All Results", command=finalSubmission, font =('Verdana', 15)).pack()
                    if float(alcoholUnits.get()) < 14:
                        forget_children(window)
                        tk.Label(window, text = "", font =('Calibri', 15)).pack()
                        tk.Label(window, text = "It is safest not to drink more than\n14 units a week on a regular basis.", font =('Verdana', 15)).pack()
                        tk.Label(window, text = "Spread your drinking evenly over three\nor more days, or you'll increase your\nrisk of long-term illness and injury.", font =('Verdana', 15)).pack()
                        tk.Button(window,text="Next", command=airQuality, font =('Verdana', 15)).pack()
                    else:
                        forget_children(window)
                        tk.Label(window, text = "", font =('Calibri', 15)).pack()
                        tk.Label(window, text = "More than 14 units a week can be\nvery unhealthy, according to the CMO's guidelines.", font =('Verdana', 15)).pack()
                        tk.Label(window, text = "Try to cut down on this amount by having\na few drink free days per week.", font =('Verdana bold', 15)).pack()
                        tk.Button(window,text="Next", command=airQuality, font =('Verdana', 15)).pack()
                forget_children(window)
                tk.Label(window, text = "How many units of alcohol\ndo you drink per week?", font =('Verdana', 15)).pack()
                tk.Label(window, text = "1 unit = 218ml standard cider\n76ml standard wine\n25ml standard whiskey\n250ml standard beer\n250ml standard alcopop", font =('Verdana', 15)).pack()
                alcoholUnits = Entry(window,width=40)
                alcoholUnits.pack()
                tk.Button(window,text="Submit", command=alcoholCalc, font =('Verdana', 15)).pack()
            def smokerYes():
                forget_children(window)
                global smokingStatus
                smokingStatus = 'Yes'
                tk.Label(window, text = "", font =('Calibri', 15)).pack()
                tk.Label(window, text = "Smoking damages your heart and blood circulation,\nincreasing the risk of conditions such as\nheart disease, heart attacks, strokes,\nperipheral vascular disease (damaged blood vessels),\nand cerebrovascular disease (damaged arteries\nthat supply blood to your brain).", font =('Verdana', 15)).pack()
                tk.Label(window, text = "Smokers have an increased risk of cancer\n(especially lung cancer) and COPD.", font =('Verdana bold', 15)).pack()
                link1 = tk.Button(window,text="NHS Quit Smoking Site", font =('Verdana', 15))
                link1.pack()
                link1.bind("<Button-1>", lambda e: callback("https://www.nhs.uk/live-well/quit-smoking/10-self-help-tips-to-stop-smoking/"))
                tk.Button(window,text="Next", command=alcohol, font =('Verdana', 15)).pack()
            def smokerNo():
                forget_children(window)
                global smokingStatus
                smokingStatus = 'No'
                tk.Label(window, text = "", font =('Calibri', 15)).pack()
                tk.Label(window, text = "Excellent! Not smoking is a great way to\nprotect yourself from cancer, heart\nand lung disease.", font =('Verdana', 15)).pack()
                tk.Button(window,text="Next", command=alcohol, font =('Verdana', 15)).pack()
            forget_children(window)
            tk.Label(window, text = "", font =('Calibri', 15)).pack()
            tk.Label(window, text = "Select one of the following:", font =('Verdana', 15)).pack()
            tk.Button(window,text="I am a Smoker", command=smokerYes, font =('Verdana', 15)).pack()
            tk.Button(window,text="I am not a Smoker", command=smokerNo, font =('Verdana', 15)).pack()
        forget_children(window)
        if weight.get() == '' or height.get() == '':
            bmi = 0
        else:
            bmi = round(float(float(weight.get()) / ((float(height.get())/100)**2)),1)
        tk.Label(window, text = "", font =('Calibri', 15)).pack()
        tk.Label(window, text = "Your BMI is "+str(bmi)+'.', font =('Verdana bold', 15)).pack()
        if bmi < 18.5:
            tk.Label(window, text = "You are underweight.", font =('Verdana bold', 15)).pack()
            tk.Label(window, text = "Try increasing your caloric intake.", font =('Verdana', 15)).pack()
            tk.Label(window, text = "If you suffer from a chronic illness, or your\nweight loss has been sudden, see your GP.", font =('Verdana', 15)).pack()
        elif bmi >= 18.5 and bmi <= 25:
            tk.Label(window, text = "Your BMI is normal/healthy!", font =('Verdana bold', 15)).pack()
            tk.Label(window, text = "Continue eating a healthy, balanced diet\nwith plenty of fruits and vegetables.\nKeep exercising regularly!", font =('Verdana', 15)).pack()
        elif bmi > 25 and bmi <= 15:
            tk.Label(window, text = "You are overweight.", font =('Verdana bold', 15)).pack()
            tk.Label(window, text = "Try and reduce your caloric intake, and\nincrease your amounts of exercise.", font =('Verdana', 15)).pack()
        elif bmi > 15 and bmi <= 40:
            tk.Label(window, text = "Your BMI shows that you are obese.", font =('Verdana bold', 15)).pack()
            tk.Label(window, text = "If you have already tried calorie restriction\nand increased exercise, please make\nan appointment to see your GP.", font =('Verdana', 15)).pack()
        elif bmi > 40:
            tk.Label(window, text = "Your BMI is in the morbidly obese range.", font =('Verdana bold', 15)).pack()
            tk.Label(window, text = "If you have not already done so, please make an\nappointment to see your GP as soon as possible.", font =('Verdana', 15)).pack()
        tk.Label(window, text = "", font =('Calibri', 15)).pack()
        tk.Button(window,text="Next", command=smoker, font =('Verdana', 15)).pack()
    forget_children(window)
    tk.Label(window, text = "", font =('Calibri', 15)).pack()
    tk.Label(window, text = "Enter your height in cm:", font =('Verdana', 15)).pack()
    height = Entry(window,width=40)
    height.pack()
    tk.Label(window, text = "Enter your weight in kg:", font =('Verdana', 15)).pack()
    weight = Entry(window,width=40)
    weight.pack()
    tk.Button(window,text="Submit", command=bmiCalc, font =('Verdana', 15)).pack()

    
def covid19():
    def CovidInfo():
        def covidInfoPage2():
            forget_children(window)
            tk.Label(window, text = "", font =('Calibri', 15)).pack()
            tk.Label(window, text = "Don't:", font =('Verdana bold', 15)).pack()
            tk.Label(window, text = "- Visit high risk destinations, with many cases.", font =('Verdana', 15)).pack()
            tk.Label(window, text = "- Touch sensitive areas, such as your eyes,\nnose or mouth, if unclean.", font =('Verdana', 15)).pack()
            tk.Label(window, text = "", font =('Calibri', 15)).pack()
            tk.Label(window, text = "Stay in isolation for 7 days if you feel you\nare exhibiting symptoms of COVID-19.", font =('Verdana bold', 15)).pack()
            tk.Button(window,text="Page 1", command=CovidInfo, font =('Verdana', 15)).pack()
            tk.Button(window,text="Home", command=covid19, font =('Verdana', 15)).pack()
        forget_children(window)
        tk.Label(window, text = "", font =('Calibri', 15)).pack()
        tk.Label(window, text = "COVID-19 INFO", font =('Verdana bold', 18)).pack()
        tk.Label(window, text = "", font =('Calibri', 15)).pack()
        tk.Label(window, text = "Don't forget to:", font =('Verdana bold', 15)).pack()
        tk.Label(window, text = "- Wash hands with soap and water for at least 20 seconds.", font =('Verdana', 15)).pack()
        tk.Label(window, text = "- Wash hands whenever you reach a new destination\nafter commuting.", font =('Verdana', 15)).pack()
        tk.Label(window, text = "- Use hand sanitiser and single-use tissues.\nThrow tissues away once used.", font =('Verdana', 15)).pack()
        tk.Label(window, text = "- Avoid close contact with people who are unwell\nand cover your mouth and nose when sneezing.", font =('Verdana', 15)).pack()
        tk.Button(window,text="Page 2", command=covidInfoPage2, font =('Verdana', 15)).pack()
    forget_children(window)
    tk.Label(window, text = "", font =('Calibri', 15)).pack()
    tk.Label(window, text = "Click the Button for:", font =('Verdana', 15)).pack()
    tk.Button(window,text="Preventative Advice about COVID-19?", command=CovidInfo, font =('Verdana', 15)).pack()
    tk.Label(window, text = "", font =('Calibri', 15)).pack()
    tk.Label(window, text = "If you think you have symptoms,\nor are affected by COVID-19,\nfollow this link:", font =('Verdana', 15)).pack()
    link1 = tk.Button(window,text="NHS 111", font =('Verdana', 15))
    link1.pack()
    link1.bind("<Button-1>", lambda e: callback("https://111.nhs.uk/service/COVID-19"))
    tk.Button(window,text="Back", command=main, font =('Verdana', 15)).pack()

def noResponse1():
    def submitEmail1():
        name = Firstname.get()
        lastname = Surname.get()
        dateob = DOB.get()
        docname = doctorName.get()
        docmail = doctorEmail.get()
        tele = telephone.get()
        condition = 'high blood sugar readings'
        mailto1(name, lastname, dateob, docname, docmail, tele, condition)
        tk.Label(window, text = "", font =('Calibri', 15)).pack()
        tk.Label(window, text = "Your email should be open in your client.", font =('Verdana', 15)).pack()
        tk.Button(window,text="Back", command=main, font =('Verdana', 15)).pack()
    forget_children(window)
    tk.Label(window, text = "", font =('Calibri', 15)).pack()
    tk.Label(window, text = "Please enter your details below\nso someone from your GP practice can call:", font =('Verdana', 15)).pack()
    tk.Label(window, text = "", font =('Calibri', 15)).pack()
    tk.Label(window, text = "First Name:", font =('Verdana', 15)).pack()
    Firstname = Entry(window,width=40)
    Firstname.pack()
    tk.Label(window, text = "Surname:", font =('Verdana', 15)).pack()
    Surname = Entry(window,width=40)
    Surname.pack()
    tk.Label(window, text = "Date Of Birth (DD/MM/YYYY):", font =('Verdana', 15)).pack()
    DOB = Entry(window,width=40)
    DOB.pack()
    tk.Label(window, text = "Phone Number of Patient:", font =('Verdana', 15)).pack()
    telephone = Entry(window,width=40)
    telephone.pack()
    tk.Label(window, text = "Doctor's Surname:", font =('Verdana', 15)).pack()
    doctorName = Entry(window,width=40)
    doctorName.pack()
    tk.Label(window, text = "Doctor's Email:", font =('Verdana', 15)).pack()
    doctorEmail = Entry(window,width=40)
    doctorEmail.pack()
    tk.Button(window,text="Submit", command=submitEmail1, font =('Verdana', 15)).pack()

def noResponse2():
    def submitEmail1():
        name = Firstname.get()
        lastname = Surname.get()
        dateob = DOB.get()
        docname = doctorName.get()
        docmail = doctorEmail.get()
        tele = telephone.get()
        condition = 'a persistent cough and breathlessness'
        mailto1(name, lastname, dateob, docname, docmail, tele, condition)
        tk.Label(window, text = "", font =('Calibri', 15)).pack()
        tk.Label(window, text = "Your email should be open in your client.", font =('Verdana', 15)).pack()
        tk.Button(window,text="Back", command=main, font =('Verdana', 15)).pack()
    forget_children(window)
    tk.Label(window, text = "", font =('Calibri', 15)).pack()
    tk.Label(window, text = "Please enter your details below\nso someone from your GP practice can call:", font =('Verdana', 15)).pack()
    tk.Label(window, text = "", font =('Calibri', 15)).pack()
    tk.Label(window, text = "First Name:", font =('Verdana', 15)).pack()
    Firstname = Entry(window,width=40)
    Firstname.pack()
    tk.Label(window, text = "Surname:", font =('Verdana', 15)).pack()
    Surname = Entry(window,width=40)
    Surname.pack()
    tk.Label(window, text = "Date Of Birth (DD/MM/YYYY):", font =('Verdana', 15)).pack()
    DOB = Entry(window,width=40)
    DOB.pack()
    tk.Label(window, text = "Phone Number of Patient:", font =('Verdana', 15)).pack()
    telephone = Entry(window,width=40)
    telephone.pack()
    tk.Label(window, text = "Doctor's Surname:", font =('Verdana', 15)).pack()
    doctorName = Entry(window,width=40)
    doctorName.pack()
    tk.Label(window, text = "Doctor's Email:", font =('Verdana', 15)).pack()
    doctorEmail = Entry(window,width=40)
    doctorEmail.pack()
    tk.Button(window,text="Submit", command=submitEmail1, font =('Verdana', 15)).pack()

def noResponse3():
    def submitEmail1():
        name = Firstname.get()
        lastname = Surname.get()
        dateob = DOB.get()
        docname = doctorName.get()
        docmail = doctorEmail.get()
        tele = telephone.get()
        condition = 'high blood pressure readings'
        mailto1(name, lastname, dateob, docname, docmail, tele, condition)
        tk.Label(window, text = "", font =('Calibri', 15)).pack()
        tk.Label(window, text = "Your email should be open in your client.", font =('Verdana', 15)).pack()
        tk.Button(window,text="Back", command=main, font =('Verdana', 15)).pack()
    forget_children(window)
    tk.Label(window, text = "", font =('Calibri', 15)).pack()
    tk.Label(window, text = "Please enter your details below\nso someone from your GP practice can call:", font =('Verdana', 15)).pack()
    tk.Label(window, text = "", font =('Calibri', 15)).pack()
    tk.Label(window, text = "First Name:", font =('Verdana', 15)).pack()
    Firstname = Entry(window,width=40)
    Firstname.pack()
    tk.Label(window, text = "Surname:", font =('Verdana', 15)).pack()
    Surname = Entry(window,width=40)
    Surname.pack()
    tk.Label(window, text = "Date Of Birth (DD/MM/YYYY):", font =('Verdana', 15)).pack()
    DOB = Entry(window,width=40)
    DOB.pack()
    tk.Label(window, text = "Phone Number of Patient:", font =('Verdana', 15)).pack()
    telephone = Entry(window,width=40)
    telephone.pack()
    tk.Label(window, text = "Doctor's Surname:", font =('Verdana', 15)).pack()
    doctorName = Entry(window,width=40)
    doctorName.pack()
    tk.Label(window, text = "Doctor's Email:", font =('Verdana', 15)).pack()
    doctorEmail = Entry(window,width=40)
    doctorEmail.pack()
    tk.Button(window,text="Submit", command=submitEmail1, font =('Verdana', 15)).pack()

   
def repeat():
    def submitEmail():
        name = Firstname.get()
        lastname = Surname.get()
        dateob = DOB.get()
        docname = doctorName.get()
        docmail = doctorEmail.get()
        nhsnum = nhsNumber.get()
        remaindays = daysLeft.get()
        mailto(name, lastname, dateob, docname, docmail, nhsnum, remaindays)
        tk.Label(window, text = "", font =('Calibri', 15)).pack()
        tk.Label(window, text = "Your email should be open in your client.", font =('Verdana', 15)).pack()
        tk.Button(window,text="Back", command=main, font =('Verdana', 15)).pack()
    forget_children(window)
    tk.Label(window, text = "", font =('Calibri', 10)).pack()
    tk.Label(window, text = "Enter your details below:", font =('Verdana', 12)).pack()
    tk.Label(window, text = "", font =('Calibri', 10)).pack()
    tk.Label(window, text = "First Name:", font =('Verdana', 12)).pack()
    Firstname = Entry(window,width=40)
    Firstname.pack()
    tk.Label(window, text = "Surname:", font =('Verdana', 12)).pack()
    Surname = Entry(window,width=40)
    Surname.pack()
    tk.Label(window, text = "Date Of Birth (DD/MM/YYYY):", font =('Verdana', 12)).pack()
    DOB = Entry(window,width=40)
    DOB.pack()
    tk.Label(window, text = "NHS Number of Patient:", font =('Verdana', 12)).pack()
    nhsNumber = Entry(window,width=40)
    nhsNumber.pack()
    tk.Label(window, text = "Days Left of Medication:", font =('Verdana', 12)).pack()
    daysLeft = Entry(window,width=40)
    daysLeft.pack()
    tk.Label(window, text = "Doctor's Surname:", font =('Verdana', 12)).pack()
    doctorName = Entry(window,width=40)
    doctorName.pack()
    tk.Label(window, text = "Doctor's Email:", font =('Verdana', 12)).pack()
    doctorEmail = Entry(window,width=40)
    doctorEmail.pack()
    tk.Button(window,text="Submit", command=submitEmail, font =('Verdana', 12)).pack()
    
def startChat():
    def reportGenerate():
        forget_children(window)
        tk.Label(window, text = "", font =('Calibri', 15)).pack()
        tk.Label(window, text = "Generating a report...", font =('Verdana', 15)).pack()
        now = datetime.now()
        measured = float(selfmeasurement.get())
        formattedDate = now.strftime("%d-%m-%Y,%H:%M:%S")
        filename = "symptomReport"+formattedDate+".txt"
        if measured < 35:
            message = "Your temperature is very low. Call Emergency Services if you are shivering as you may be suffering from Hypothermia."
        elif measured >= 35 and measured < 37:
            message = "Your temperature is low. Drink warm fluids and stay warm!"
        elif measured >= 37 and measured < 38:
            message = "Your temperature is normal. You should be healthy!"
            tk.Label(window, text = "Your temperature is normal, but if you\nfeel ill, ensure you monitor it and\nmake an appointment with your GP if you\nexhibit severe symptoms.", font =('Verdana', 15)).pack()
        elif measured >= 38:
            message = "Your temperature is high. You may have a fever or infection."
            tk.Label(window, text = "Due to your temperature, you should\nmake an appointment with your GP\nin order to get an X-Ray/Blood Test.", font =('Verdana', 15)).pack()
        with open(filename, 'a')as f:
            f.write("--REPORT GENERATED ON "+formattedDate+"--\nTemperature: "+str(selfmeasurement.get())+'\n'+str(message)+'\nSymptoms: '+str(otherSymptoms.get(1.0,'end-1c')))
            f.close()
        tk.Label(window, text = "Report has been generated in the directory\nwhere this program is stored.", font =('Verdana', 15)).pack()
        tk.Button(window,text="Back", command=main, font =('Verdana', 15)).pack()
    forget_children(window)
    tk.Label(window, text = "", font =('Calibri', 15)).pack()
    tk.Label(window, text = "If you have measured a temperature yourself,\ntype the number here:", font =('Verdana', 15)).pack()
    selfmeasurement = Entry(window,width=40)
    selfmeasurement.pack()
    tk.Label(window, text = "", font =('Calibri', 15)).pack()
    tk.Label(window, text = "Are you exhibiting any other symptoms that worry you?", font =('Verdana', 15)).pack()
    otherSymptoms = tk.Text(window,width=40,height=8, borderwidth=2, relief="groove")
    otherSymptoms.pack()
    tk.Button(window,text="Submit", command=reportGenerate, font =('Verdana', 15)).pack()
    tk.Label(window, text = "", font =('Calibri', 15)).pack()
    tk.Button(window,text="Back", command=main, font =('Verdana', 15)).pack()

def newSymptom():
    forget_children(window)
    tk.Label(window, text = "", font =('Calibri', 15)).pack()
    tk.Label(window, text = "Enter your symptom here:", font =('Verdana', 15)).pack()
    searchQuery = Entry(window,width=40)
    searchQuery.pack()
    link2 = tk.Button(window,text="Submit", font =('Verdana', 15))
    link2.pack()
    link2.bind("<Button-1>", lambda e: callback("https://www.nhs.uk/search?collection=nhs-meta&query="+str(searchQuery.get())))
    tk.Label(window, text = "", font =('Calibri', 15)).pack()
    tk.Button(window,text="Back", command=main, font =('Verdana', 15)).pack()

def new():
    forget_children(window)
    tk.Label(window, text = "", font =('Calibri', 15)).pack()
    tk.Label(window, text = "Do you have a temperature sensor\nattached to the Pi?", font =('Verdana', 15)).pack()
    tk.Label(window, text = "", font =('Calibri', 15)).pack()
    tempYes = tk.Button(window,text="Yes", command=tempWindow, font =('Verdana', 15)).pack()
    tempNo = tk.Button(window,text="No", command=startChat, font =('Verdana', 15)).pack()
    tk.Button(window,text="Back", command=main, font =('Verdana', 15)).pack()

def new1():
    forget_children(window)
    tk.Label(window, text = "", font =('Calibri', 15)).pack()
    tk.Label(window, text = "Do you have a temperature sensor\nattached to the Pi?", font =('Verdana', 15)).pack()
    tk.Label(window, text = "", font =('Calibri', 15)).pack()
    tempYes = tk.Button(window,text="Yes", command=tempWindow, font =('Verdana', 15)).pack()
    tempNo = tk.Button(window,text="No", command=startChat, font =('Verdana', 15)).pack()
    tk.Button(window,text="Back", command=main, font =('Verdana', 15)).pack()

def chronic():
    forget_children(window)
    tk.Label(window, text = "", font =('Calibri', 15)).pack()
    tk.Label(window, text = "Select one of the following:", font =('Verdana', 15)).pack()
    tk.Label(window, text = "", font =('Calibri', 15)).pack()
    tk.Button(window,text="Diabetes", command=diabetes, font =('Verdana', 15)).pack()
    tk.Button(window,text="Hypertension", command=hypertension, font =('Verdana', 15)).pack()
    tk.Button(window,text="Asthma/COPD", command=asthma, font =('Verdana', 15)).pack()
    tk.Button(window,text="Other", command=other, font =('Verdana', 15)).pack()
    tk.Label(window, text = "", font =('Calibri', 15)).pack()
    tk.Button(window,text="Back", command=main, font =('Verdana', 15)).pack()

def main():
    forget_children(window)
    window.geometry('%sx%s' % (width, height))
    tk.Label(window, text = "", font =('Calibri', 15)).pack()
    label = tk.Label(window, text = "Greetings! Welcome to", font =('Verdana', 15)).pack()
    label2 = tk.Label(window, text = "My Little Doctor", font =('Verdana bold', 36)).pack()
    tk.Label(window, text = "", font =('Calibri', 15)).pack()
    tk.Button(window,text="I Want General Health Advice", command=lifestyle, font =('Verdana', 15)).pack()
    tk.Button(window,text="I Want Advice on a Chronic Illness", command=chronic, font =('Verdana', 15)).pack()
    tk.Button(window,text="I Am Worried About COVID-19", command=covid19, font =('Verdana', 15)).pack()
    tk.Button(window,text="I Have A New Symptom", command=newSymptom, font =('Verdana', 15)).pack()
    window.mainloop()
        
main()
