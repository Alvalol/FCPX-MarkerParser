
"""This program gets an XML file exported by Final Cut Pro X, gets the markers and their timecodes
 from the file and outputs a new file in a clear an concise format. Then, it sends an e-mail backup to yourself. """


import datetime
import xml.etree.ElementTree as ET
import smtplib
import sys
import os
import yaml
from email.mime.text import MIMEText
from Config import *


if not bool(config):
    print "Welcome to your first run of FCPXParser, please enter the configuration information"
    config['useremail'] = str(raw_input("Enter your email\n"))
    config['yourname'] = str(raw_input("Enter your name\n"))
    config['recipientName'] = str(raw_input("Enter your recipient's name\n"))
    config['directory'] = str(raw_input("Enter the directory as such /PATH1/PATH2/.../PATH/\n"))
    config['file'] = str(raw_input("Enter the name of the file. Exclude .fcpx extension\n"))
    stream = file('Config.py', 'w')
    yaml.dump(config,stream)
    stream.close()

else:
    stream = file('Config.py', 'r')
    config = yaml.load(stream)



tree = ET.parse(config['directory'] + config['file'] + ".fcpxml")
root = tree.getroot()

OutputFile = open(config['directory'] + 'E-mail.txt','w+')

#Goes down the element tree and initializes startValue
video = root.find('project').find('sequence').find('spine').find('video')
startValue =  eval(video.get('start').replace('s',''))

tempmarkers = []
markersNames = []
projectName = root.find('project').get('name')


for marker in video.findall('marker'):
    tempmarkers.append(marker.get('start')), \
    markersNames.append(marker.get('value'))

cleanMarkers = []
for i in tempmarkers:
    i = i.replace('s','')
    cleanMarkers.append(eval(i))
del tempmarkers

OutputFile.write("Hello " + config['recipientName'] +  " here\'s " + projectName +  "\'s project." + "\n\n")



stufftoWrite = []
for i in range(len(cleanMarkers)):
    stufftoWrite.append(((markersNames[i])) +  " :  " + ((str(datetime.timedelta(seconds=(cleanMarkers[i]-startValue))))))


for i in range(len(stufftoWrite)):
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
    password = raw_input("Enter password\n")
    sendMail()
elif Sendmail == "n":
    print "A file named E-Mail has been made at " + config['directory'] + config['file']
else:
    print "You have entered an invalid answer. Please try again"
    sys.exit(0)
