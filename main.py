
"""This program gets an XML file exported by Final Cut Pro X, gets the markers and their timecodes
 from the file and outputs a new file in a clear an concise format. Then, it sends an e-mail backup to yourself. """


import datetime
import xml.etree.ElementTree as ET
import smtplib
import sys
import os
import json
from email.mime.text import MIMEText
from Config import *
#import GUI

if os.stat("Config.py").st_size ==0:
    config = {}
    print "Welcome to your first run of FCPXParser, please enter the configuration information"
    config['useremail'] = str(raw_input("Enter your gmail account\n"))
    while "@gmail.com" not in config['useremail']:
        config['useremail'] = str(raw_input("Enter your gmail account\n"))

    config['yourname'] = str(raw_input("Enter your name\n"))
    config['recipientName'] = str(raw_input("Enter your recipient's name\n"))
    config['directory'] = str(raw_input("Enter the directory as such /PATH1/PATH2/.../PATH/\n"))
    config['file'] = str(raw_input("Enter the name of the file. Exclude .fcpx extension\n"))
    with open("Config.py",'w') as f: f.write(json.dumps(config))
    f.close()
    with open("Config.py","r") as f:
        config = json.load(f)
    f.close()
else:
    with open("Config.py","r") as f:
        config = json.load(f)
    f.close()

tree = ET.parse(config['directory'] + config['file'] + ".fcpxml")
root = tree.getroot()

OutputFile = open(config['directory'] + 'E-mail.txt','w+')

#Goes down the element tree and initializes startValue
video = root.find('project').find('sequence').find('spine').find('video')
startValue =  ast.literal_eval(video.get('start').replace('s',''))

markersNames = []
projectName = root.find('project').get('name')


for marker in video.findall('marker'):
    tempmarkers.append(marker.get('start'))
    markersNames.append(marker.get('value'))

cleanMarkers = []
for i in markers:
    i = i.replace('s','')
    markers.append(ast.literal_eval(i))


OutputFile.write("Hello " + config['recipientName'] +  " here's " + projectName +  "'s project." + "\n\n")


stufftoWrite = []
for i in enumerate(cleanMarkers, start=0):
    stufftoWrite.append(((markersNames[i])) +  " :  " + ((str(datetime.timedelta(seconds=(cleanMarkers[i]-startValue))))))


for i in enumerate(stufftoWrite, start=0):
    OutputFile.write(str(stufftoWrite[i]+ "\n"))
OutputFile.write("\n\nThanks, " + config['yourname'])
OutputFile.close()


def sendMail():
    fp = open(config['directory'] + 'E-mail.txt', 'r')
    msg = MIMEText(fp.read())
    fp.close()

    msg['Subject'] =  projectName
    msg['From'] = config['useremail']
    msg['To'] = config['useremail']
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()
    server.login(config['useremail'],password)
    server.sendmail(config['useremail'],config['useremail'],msg.as_string())
    server.quit()
    print "A copy of the form has been sent to " + config['useremail']


Sendmail = raw_input("Send e-mail? Y/N only\n").lower()
if Sendmail == "y":
    password = raw_input("Enter password for " + config['useremail'] + "\n")
    sendMail()
elif Sendmail == "n":
    print "A file named E-Mail has been made at " + config['directory'] + config['file']
else:
    print "You have entered an invalid answer. Please try again"
    sys.exit(0)
